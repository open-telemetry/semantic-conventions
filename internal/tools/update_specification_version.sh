#!/bin/bash

# Example usage:
#
# ./internal/tools/update_specification_version.sh


# Set this to the version number you want to CHANGE in URLs in the repository.
PREVIOUS_SPECIFICATION_VERSION="v1.22.0"
# Set this to the version number you want to KEEP in URLs in the repository.
LATEST_SPECIFICATION_VERSION="v1.26.0"
# The specific pattern we look for when replacing URLs
SPECIFICATION_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/tree/"
SPECIFICATION_BLOB_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/blob/"


fix_file() {
  echo Fixing file $1
  sed -i \
   -e "s,${SPECIFICATION_URL_PREFIX}${PREVIOUS_SPECIFICATION_VERSION},${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATION_VERSION},g" \
   -e "s,${SPECIFICATION_BLOB_URL_PREFIX}${PREVIOUS_SPECIFICATION_VERSION},${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATION_VERSION},g" \
   "$1"
}

important_files=("docs" "model" "README.md" "supplementary-guidelines")

# TODO - limit to markdown/yaml files?
find "${important_files[@]}" -type f -not -path '*/.*' -print0 | while read -d $'\0' file; do
  fix_file "$file"
done
