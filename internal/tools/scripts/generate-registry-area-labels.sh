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
AREAS=$1

echo -e "\nStarting to create area labels"
echo -e "--------------------------------\n"

while IFS= read -r label; do
    if (( "${#label}" > 50 )); then
        echo -e "Label $label exceeds GitHubs 50-character limit on labels, skipping"
        continue
    fi
    echo "$label"
    gh label create "$label" -c "#425cc7" --force
done < ${AREAS}

echo -e "\nLabels created successfully"
echo -e "--------------------------------\n"

