
#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt


MARKDOWN_EXTENSIONS = {
    ".md",
    ".mkd",
    ".mdx",
    ".mdown",
    ".mdwn",
    ".mkdn",
    ".mkdown",
    ".markdown",
}


class HTMLLinkParser(HTMLParser):
    """Extract link destinations from HTML elements."""

    def __init__(self):
        super().__init__()
        self.destinations = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if value and name.lower() in ("href", "src"):
                self.destinations.append(value)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def normalize_path(path):
    """Normalize a repository-relative path."""
    return path.replace("\\", "/")


def resolve_destination(destination, source_file, repo_root):
    """Resolve an internal link to a repository-relative path."""
    destination = destination.strip()

    if not destination:
        return None

    parsed = urlsplit(destination)

    # Ignore external URLs, mail addresses and other URI schemes.
    if parsed.scheme or parsed.netloc:
        return None

    path = unquote(parsed.path)

    if not path:
        return None

    if path.startswith("/"):
        resolved = repo_root / path.lstrip("/")
    else:
        resolved = source_file.parent / path

    try:
        return normalize_path(
            resolved.resolve().relative_to(repo_root.resolve()).as_posix()
        )
    except ValueError:
        # The destination points outside the repository.
        return None


def extract_destinations(content, markdown):
    """Extract Markdown and embedded HTML link destinations."""
    destinations = []

    for token in markdown.parse(content):
        if token.type == "inline" and token.children:
            for child in token.children:
                if child.type == "link_open":
                    href = child.attrGet("href")
                    if href:
                        destinations.append(href)

                elif child.type == "image":
                    src = child.attrGet("src")
                    if src:
                        destinations.append(src)

                elif child.type == "html_inline":
                    html_parser = HTMLLinkParser()
                    html_parser.feed(child.content)
                    destinations.extend(html_parser.destinations)

        elif token.type == "html_block":
            html_parser = HTMLLinkParser()
            html_parser.feed(token.content)
            destinations.extend(html_parser.destinations)

    return destinations


def main():
    parser = argparse.ArgumentParser(
        description="Find Markdown files linking to changed files."
    )

    parser.add_argument(
        "--root",
        default=".",
        help="Repository root directory.",
    )

    target_group = parser.add_mutually_exclusive_group(required=True)

    target_group.add_argument(
        "--targets",
        nargs="+",
        help="Changed repository-relative file paths.",
    )

    target_group.add_argument(
        "--targets-file",
        help="File containing NUL-separated changed file paths.",
    )

    parser.add_argument(
        "--search-dir",
        default=".",
        help="Directory containing Markdown files to scan.",
    )

    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    search_dir = (repo_root / args.search_dir).resolve()

    # Read changed file paths.
    if args.targets_file:
        try:
            target_data = Path(args.targets_file).read_bytes()
        except OSError as error:
            print(
                "Cannot read targets file: {}".format(error),
                file=sys.stderr,
            )
            return 1

        target_values = [
            path.decode("utf-8")
            for path in target_data.split(b"\0")
            if path
        ]
    else:
        target_values = args.targets

    # Normalize changed paths relative to the repository root.
    targets = set()

    for target in target_values:
        target_path = (repo_root / target).resolve()

        try:
            relative_path = target_path.relative_to(repo_root).as_posix()
            targets.add(normalize_path(relative_path))
        except ValueError:
            print(
                "Warning: target is outside repository: {}".format(target),
                file=sys.stderr,
            )

    if not targets:
        return 0

    # Validate the search directory.
    if not search_dir.is_dir():
        print(
            "Search directory does not exist: {}".format(search_dir),
            file=sys.stderr,
        )
        return 1

    try:
        relative_search_dir = search_dir.relative_to(repo_root)
    except ValueError:
        print(
            "Search directory is outside repository: {}".format(search_dir),
            file=sys.stderr,
        )
        return 1

    # Obtain tracked and untracked files from Git.
    # Ignored files and directories are excluded.
    try:
        result = subprocess.run(
            [
                "git",
                "ls-files",
                "-z",
                "--cached",
                "--others",
                "--exclude-standard",
            ],
            cwd=repo_root,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        print(
            "Cannot list repository files with Git: {}".format(error),
            file=sys.stderr,
        )
        return 1

    markdown = MarkdownIt("commonmark", {"html": True})
    incoming_files = set()

    # Git uses NUL separators to handle paths containing spaces safely.
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue

        relative_source = Path(os.fsdecode(raw_path))

        # Only scan Markdown files.
        if relative_source.suffix.lower() not in MARKDOWN_EXTENSIONS:
            continue

        # Respect the optional search directory.
        try:
            relative_source.relative_to(relative_search_dir)
        except ValueError:
            continue

        source_file = repo_root / relative_source

        # Ignore files that no longer exist in the working tree.
        if not source_file.is_file():
            continue

        # Do not scan Git metadata.
        if ".git" in relative_source.parts:
            continue

        try:
            content = source_file.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(
                "Warning: cannot read {}: {}".format(source_file, error),
                file=sys.stderr,
            )
            return 1

        for destination in extract_destinations(content, markdown):
            resolved = resolve_destination(
                destination,
                source_file,
                repo_root,
            )

            if resolved in targets:
                incoming_files.add(relative_source.as_posix())
                break

    # Print files containing incoming links.
    for file_path in sorted(incoming_files):
        print(file_path)

    return 0


if __name__ == "__main__":
    sys.exit(main())
