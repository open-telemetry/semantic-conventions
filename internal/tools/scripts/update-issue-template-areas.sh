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

CUR_DIRECTORY=$(dirname "$0")
REPO_DIR="$( cd "$CUR_DIRECTORY/../../../" && pwd )"
GITHUB_DIR="$( cd "$REPO_DIR/.github/" && pwd )"
TEMPLATES_DIR="$( cd "$GITHUB_DIR/ISSUE_TEMPLATE" && pwd )"

AREAS=$(sh "${GITHUB_DIR}/workflows/scripts/get-registry-areas.sh")

START_AREA_LIST="# Start semconv area list"
END_AREA_LIST="# End semconv area list"

replacement="      ${START_AREA_LIST}"

for AREA in ${AREAS}; do
    LABEL_NAME=$(basename "${AREA}" .yaml)
   replacement="${replacement}\n      - area:${LABEL_NAME}"
done

echo -e "\nStarting to replace areas in ISSUE_TEMPLATES:"
echo -e "---------------------------------------------\n"

replacement="${replacement}\n      ${END_AREA_LIST}"

echo -e "The replacement text will be:"
echo -e "---------------------------------------------\n"
echo -e $replacement

find ${TEMPLATES_DIR} -type f -name '*.yaml' -exec sed -i "/$START_AREA_LIST/,/$END_AREA_LIST/c\\$replacement" {} \;

echo -e "\nISSUE_TEMPLATES updated successfully"
echo -e "---------------------------------------------"
