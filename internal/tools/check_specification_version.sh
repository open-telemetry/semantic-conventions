#!/bin/bash

# Example usage:
#
# ./internal/tools/check_specification_version.sh

# Set this to the version number you want to CHECK in URLs in the repository.
LATEST_SPECIFICATION_VERSION="v1.22.0"

# The specific pattern we look for when checking URLs
SPECIFICATION_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/tree/"
SPECIFICATION_BLOB_URL_PREFIX="https://github.com/open-telemetry/opentelemetry-specification/blob/"

# Check all links to the specification to ensure they are using the latest version
find . -type f -not -path '*/.*' -print0 | while read -d $'\0' file; do
  if grep -q "${SPECIFICATION_URL_PREFIX}[^/]*" "$file"; then
    grep -q "${SPECIFICATION_URL_PREFIX}${LATEST_SPECIFICATION_VERSION}" "$file" || echo "File $file contains a link to the OpenTelemetry specification that is not using the latest version."
  fi

  if grep -q "${SPECIFICATION_BLOB_URL_PREFIX}[^/]*" "$file"; then
    grep -q "${SPECIFICATION_BLOB_URL_PREFIX}${LATEST_SPECIFICATION_VERSION}" "$file" || echo "File $file contains a link to the OpenTelemetry specification that is not using the latest version."
  fi
done