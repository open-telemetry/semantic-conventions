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
AREAS=$(sh "${CUR_DIRECTORY}/get-registry-areas.sh")

echo -e "\nStarting to create area labels"
echo -e "--------------------------------\n"

for AREA in ${AREAS}; do
    LABEL_NAME=$(basename "${AREA}" .yaml)

    if (( "${#LABEL_NAME}" > 50 )); then
        echo "'${LABEL_NAME}' exceeds GitHubs 50-character limit on labels, skipping"
        continue
    fi
    echo "area:${LABEL_NAME}"

    #  gh label create "area:${LABEL_NAME}" -c "#425cc7"
done

echo -e "\nLabels created successfully"
echo -e "--------------------------------\n"

