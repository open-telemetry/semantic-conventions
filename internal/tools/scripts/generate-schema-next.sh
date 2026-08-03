#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# Generate header and `{next_version}:` section in next schema yaml based on weaver
# diff output.

set -euo pipefail

cur_version="$1"
prev_version="$2"
diff_file="$3"
cur_version_schema_file="schemas/$cur_version"
prev_version_schema_file="schemas/$prev_version"

# Check if the previous version schema file exists
if [[ ! -f "$prev_version_schema_file" ]]; then
  echo "Previous version schema file not found: $prev_version_schema_file"
  exit 1
fi

# check if the current version schema file exists
if [[ -f "$cur_version_schema_file" ]]; then
  echo "Current version schema file already exists: $cur_version_schema_file"
  exit 1
fi

if ! grep -q "^versions:$" "$prev_version_schema_file"; then
  echo "String 'versions:' not found in the file $prev_version_schema_file."
  exit 1
fi

prev_header_lines=$(awk '/^versions:/{print NR; exit}' "$prev_version_schema_file")

# need to replace the next_version_placeholder in the header file due to https://github.com/open-telemetry/weaver/issues/775
# TODO: remove it after the issue is fixed
{
  sed "s/next_version_placeholder/$cur_version/g" "$diff_file"
  tail -n +"$((prev_header_lines + 1))" "$prev_version_schema_file"
} > "$cur_version_schema_file"