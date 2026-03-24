#!/bin/bash

# Example usage:
#
# ./internal/tools/update-spec-repo-links.sh v1.41.0

# Set this to the version number you want to KEEP in URLs in the repository.
LATEST_SPECIFICATION_VERSION=$1
# The specific pattern we look for when replacing URLs
SPECIFICATION_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/blob/"
# The specific pattern we look for updating the Badge with the spec version
SPECIFICATION_BADGE_PREFIX="https://img.shields.io/badge/OTel_specification_version-"
SPECIFICATION_BADGE_RELEASE_TAG_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/releases/tag/"

fix_file() {
  echo Fixing file "$1"

  # Replace any versioned spec URL/badge with the latest version.
  # Uses a negative lookahead to skip URLs pointing to semantic_conventions/
  # paths that were moved from the spec repo and no longer exist in newer versions.
  perl -pi -e "
    s,\Q${SPECIFICATION_URL_PREFIX}\Ev1\.\d+\.\d+(?=/specification/(?!.*/semantic_conventions/)),${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATION_VERSION},g;
    s,\Q${SPECIFICATION_BADGE_PREFIX}\Ev1\.\d+\.\d+,${SPECIFICATION_BADGE_PREFIX}${LATEST_SPECIFICATION_VERSION},g;
    s,\Q${SPECIFICATION_BADGE_RELEASE_TAG_PREFIX}\Ev1\.\d+\.\d+,${SPECIFICATION_BADGE_RELEASE_TAG_PREFIX}${LATEST_SPECIFICATION_VERSION},g;
  " "$1"
}

important_files=("docs" "model" "README.md")

# TODO - limit to markdown/yaml files?
find "${important_files[@]}" -type f -not -path '*/.*' -not -path '*.png' -print0 | while read -d $'\0' file; do
  fix_file "$file"
done
