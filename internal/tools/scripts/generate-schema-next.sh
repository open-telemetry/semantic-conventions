#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# Generate `{next_version}:` section in next schema yaml based on weaver diff output.

set -euo pipefail

cur_version=$1
prev_version=$2
cur_version_schema_file="schemas/$cur_version"
prev_version_schema_file="schemas/$prev_version"
changes_file_content=$(< $3)

# Check if the previous version schema file exists
if [[ ! -f ${prev_version_schema_file} ]]; then
  echo "Previous version schema file not found: ${prev_version_schema_file}"
  exit 1
fi

# check if the current version schema file exists
if [[ -f ${cur_version_schema_file} ]]; then
  echo "Current version schema file already exists: ${cur_version_schema_file}"
  exit 1
fi

if ! grep -q "^versions:$" ${prev_version_schema_file}; then
  echo "String 'versions:' not found in the file ${prev_version_schema_file}."
  exit 1
fi

cp ${prev_version_schema_file} ${cur_version_schema_file}

sed -i "s/^schema_url: .*/schema_url: https:\/\/opentelemetry.io\/schemas\/$cur_version/" ${cur_version_schema_file}

echo -e "Updating ${cur_version_schema_file} with changes:\\n $changes_file_content"

changes_file_content_escaped=$(echo "${changes_file_content}" | sed ':a;N;$!ba;s/\n/\\n/g')
sed -i "s/^versions:/versions:\\n  ${cur_version}:${changes_file_content_escaped}/"  ${cur_version_schema_file}
