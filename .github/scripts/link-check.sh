#!/bin/bash

set -e

export MSYS_NO_PATHCONV=1 # for Git Bash on Windows

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../.."
DEPENDENCIES_DOCKERFILE="$ROOT_DIR/dependencies.Dockerfile"

# Parse command line arguments
LOCAL_LINKS_ONLY=false
CONFIG_FILE=".github/scripts/lychee-config.toml"
VERBOSE=true
TARGET=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --local-links-only)
            LOCAL_LINKS_ONLY=true
            shift
            ;;
        --config)
            if [[ $# -lt 2 ]]; then
                echo "Missing value for --config" >&2
                exit 1
            fi
            CONFIG_FILE=$2
            shift 2
            ;;
        --no-verbose)
            VERBOSE=false
            shift
            ;;
        *)
            # Treat any other arguments as file paths
            TARGET="$TARGET $1"
            shift
            ;;
    esac
done

# Extract lychee version from dependencies.dockerfile
LYCHEE_VERSION=$(grep "FROM lycheeverse/lychee:" "$DEPENDENCIES_DOCKERFILE" | sed 's/.*FROM lycheeverse\/lychee:\([^ ]*\).*/\1/')

if [[ -z "$TARGET" ]]; then
    TARGET="."
fi

# Build the lychee command with optional GitHub token
CMD="lycheeverse/lychee:$LYCHEE_VERSION --root-dir /data"

if [[ "$VERBOSE" == "true" ]]; then
    CMD="$CMD --verbose"
fi

# Add GitHub token if available
if [[ -n "$GITHUB_TOKEN" ]]; then
    CMD="$CMD --github-token $GITHUB_TOKEN"
fi

if [[ "$LOCAL_LINKS_ONLY" == "true" ]]; then
    CMD="$CMD --scheme file --include-fragments"
else
    CMD="$CMD --config $CONFIG_FILE"
fi

CMD="$CMD $TARGET"

# Determine if we should allocate a TTY
DOCKER_FLAGS="--rm --init"
if [[ -t 0 ]]; then
    DOCKER_FLAGS="$DOCKER_FLAGS -it"
else
    DOCKER_FLAGS="$DOCKER_FLAGS -i"
fi

# Run lychee with proper signal handling
exec docker run $DOCKER_FLAGS -v "$ROOT_DIR":/data -w /data $CMD
