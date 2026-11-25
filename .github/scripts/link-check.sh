#!/bin/bash

set -e

export MSYS_NO_PATHCONV=1 # for Git Bash on Windows

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../.."
DEPENDENCIES_DOCKERFILE="$ROOT_DIR/dependencies.Dockerfile"

# Default configuration
LOCAL_LINKS_ONLY=false
CONFIG_FILE=".github/scripts/lychee-config.toml"
FILES_FROM=""
TARGETS=()
ESCAPED_TARGET=""

escape_lychee_glob() {
    local input="$1"
    local output=""
    local character
    local index

    for ((index = 0; index < ${#input}; index++)); do
        character="${input:index:1}"
        case "$character" in
            '[') output+='[[]' ;;
            ']') output+='[]]' ;;
            '*') output+='[*]' ;;
            '?') output+='[?]' ;;
            *) output+="$character" ;;
        esac
    done

    ESCAPED_TARGET="$output"
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --local-links-only)
            LOCAL_LINKS_ONLY=true
            shift
            ;;
        --config)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --config" >&2
                exit 1
            fi
            CONFIG_FILE="$2"
            shift 2
            ;;
        --files-from)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --files-from" >&2
                exit 1
            fi
            if [[ -n "$FILES_FROM" ]]; then
                echo "Only one --files-from option is allowed" >&2
                exit 1
            fi
            FILES_FROM="$2"
            shift 2
            ;;
        --)
            shift
            TARGETS+=("$@")
            break
            ;;
        *)
            TARGETS+=("$1")
            shift
            ;;
    esac
done

# Read NUL-delimited file paths when provided
if [[ -n "$FILES_FROM" ]]; then
    if [[ ! -f "$FILES_FROM" ]]; then
        echo "File list not found: $FILES_FROM" >&2
        exit 1
    fi

    if [[ ${#TARGETS[@]} -gt 0 ]]; then
        echo "Do not combine --files-from with positional file paths" >&2
        exit 1
    fi

    while IFS= read -r -d '' target; do
        escape_lychee_glob "$target"
        TARGETS+=("$ESCAPED_TARGET")
    done < "$FILES_FROM"

    if [[ ${#TARGETS[@]} -eq 0 ]]; then
        echo "The file list is empty" >&2
        exit 1
    fi
fi

# Default to the entire repository when no targets are provided
if [[ ${#TARGETS[@]} -eq 0 ]]; then
    TARGETS=(".")
fi

# Extract Lychee version from dependencies.Dockerfile
LYCHEE_VERSION=$(
    grep "FROM lycheeverse/lychee:" "$DEPENDENCIES_DOCKERFILE" |
        sed 's/.*FROM lycheeverse\/lychee:\([^ ]*\).*/\1/'
)

if [[ -z "$LYCHEE_VERSION" ]]; then
    echo "Could not determine Lychee version" >&2
    exit 1
fi

# Build Docker arguments without concatenating untrusted values
DOCKER_ARGS=(
    run
    --rm
    --init
    -v "$ROOT_DIR:/data"
    -w /data
)

if [[ -t 0 && -t 1 ]]; then
    DOCKER_ARGS+=(-it)
fi

LYCHEE_ARGS=(
    --verbose
    --root-dir /data
)

# Add GitHub token when available
if [[ -n "${GITHUB_TOKEN:-}" ]]; then
    LYCHEE_ARGS+=(--github-token "$GITHUB_TOKEN")
fi

# Configure local-only or regular link checking
if [[ "$LOCAL_LINKS_ONLY" == "true" ]]; then
    LYCHEE_ARGS+=(--hidden --scheme file --include-fragments)
else
    LYCHEE_ARGS+=(--config "$CONFIG_FILE")
fi

# Preserve individual file arguments, including spaces and special characters
LYCHEE_ARGS+=(-- "${TARGETS[@]}")

# Run Lychee
exec docker "${DOCKER_ARGS[@]}" \
    "lycheeverse/lychee:$LYCHEE_VERSION" \
    "${LYCHEE_ARGS[@]}"
