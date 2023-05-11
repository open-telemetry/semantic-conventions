#!/bin/bash

# Example usage:
#
# ./internal/tools/update_specification_version.sh


# Set this to the version number you want to CHANGE in URLs in the repository.
PREVIOUS_SPECIFICATION_VERSION="main"
# Set this tot he version number you want to KEEP in URLs in the repository.
LATEST_SPECIFICATOIN_VERSION="1.20.0"
# This the the specific pattern we look for when replacing URLs
SPECIFICATION_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/tree/"
SPECIFICATION_BLOB_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/blob/"


fix_file() {
  echo Fixing file $1
  sed -i "s,${SPECIFICATION_URL_PREFIX}${PREVIOUS_SPECIFICATION_VERSION},${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATOIN_VERSION},g" "$1"
  sed -i "s,${SPECIFICATION_BLOB_URL_PREFIX}${PREVIOUS_SPECIFICATION_VERSION},${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATOIN_VERSION},g" "$1"
}

fix_directory() {
  # TODO - limit to markdown/yaml files?  
  for file in $(ls $1); do
    if [[ -d "$1/$file" ]]; then
      fix_directory "$1/$file"
    elif [[ -f "$1/$file" ]]; then
      fix_file "$1/$file"
    fi
  done
}

important_files=("specification" "semantic_conventions" "README.md" "supplementary-guidelines")

for file in ${important_files[@]}; do
  if [[ -d $file ]]; then
    fix_directory "$file"
  elif [[ -f $file ]]; then
    fix_file "$file"
  fi
done
