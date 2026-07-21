#!/usr/bin/env bash

# Description: This script checks if all signal groups declared in a YAML file are present in the markdown files under a specified directory.
# Usage: ./check_lines.sh <groups_list> <md_directory_path>

set -euo pipefail

groups="$1"
docs_folder="$2"

if [[ ! -f "$groups" ]]; then
  echo "File with groups does not exist: $groups"
  exit 1
fi

if [[ ! -d "$docs_folder" ]]; then
  echo "Docs folder does not exist: $docs_folder"
  exit 1
fi

declare -A semconv_snippets
# Extract only lines of the form <!-- semconv ... --> from .md files
echo "Indexing semconv lines in .md files under: $docs_folder ..."
while IFS= read -r LINE; do
  semconv_snippets["$LINE"]=1
done < <(
  find "$docs_folder" -type f -name "*.md" -exec grep -hoE '<!--[[:space:]]*semconv[[:space:]]+[a-z0-9._]+[[:space:]]*-->' {} + \
    | sed -E 's/<!--[[:space:]]*semconv[[:space:]]+([a-z0-9._]+)[[:space:]]*-->/\1/'
)

not_found_groups=()

while IFS= read -r LINE || [[ -n "$LINE" ]]; do
  if [[ -z "${semconv_snippets[$LINE]+_}" ]]; then
    not_found_groups+=("$LINE")
  fi
done < "$groups"

echo

if [[ ${#not_found_groups[@]} -gt 0 ]]; then
  echo "❌ The following signals were declared in yaml and NOT found in markdown:"
  for line in "${not_found_groups[@]}"; do
    echo " - $line"
  done
  exit 1
fi

echo "All groups were found."
