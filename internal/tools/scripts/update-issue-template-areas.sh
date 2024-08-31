#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# Create labels for all semantic convention areas that are in model/registry.
# Existing labels are not affected.
#
# Note that there is a 50-character limit on labels, so some areas may
# not have a corresponding label.

set -euo pipefail

OS=$(uname | tr '[:upper:]' '[:lower:]')

if [[ "${OS}" == "darwin" ]]; then
  SED="gsed"
else
  SED="sed"
fi

CUR_DIRECTORY=$(dirname "$0")
REPO_DIR="$( cd "$CUR_DIRECTORY/../../../" && pwd )"
GITHUB_DIR="$( cd "$REPO_DIR/.github/" && pwd )"
TEMPLATES_DIR="$( cd "$GITHUB_DIR/ISSUE_TEMPLATE" && pwd )"

AREAS=$1

START_AREA_LIST="# Start semconv area list"
END_AREA_LIST="# End semconv area list"

replacement="        ${START_AREA_LIST}"

while IFS= read -r line; do
  replacement="${replacement}\n        - $line"
done < ${AREAS}

echo -e "\nStarting to replace areas in ISSUE_TEMPLATES:"
echo -e "---------------------------------------------\n"

replacement="${replacement}\n        ${END_AREA_LIST}"

echo -e "The replacement text will be:"
echo -e "---------------------------------------------\n"
echo -e $replacement

find ${TEMPLATES_DIR} -type f -name '*.yaml'  -print0 | xargs -0 ${SED} -i "/$START_AREA_LIST/,/$END_AREA_LIST/c\\$replacement"

echo -e "\nISSUE_TEMPLATES updated successfully"
echo -e "---------------------------------------------"
