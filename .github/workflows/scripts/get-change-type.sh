#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0


# This script gets change type from chloggen file.
# If there are none or multiple changelog files, it will return 1.

if [ -z ${PR:-} ]; then
    echo "PR number is required"
    exit 1
fi

CHLOG="$(gh pr view $PR --json files --jq '.files.[].path | select (. | startswith(".chloggen/"))')"
# echo "Change log file(s): ${CHLOG}"

if [ -z "$CHLOG" ]; then
    echo "No changelog found in the PR. Ignoring this change."
    exit 1
fi

COUNT="$(echo "$CHLOG" | wc -l)"
if [ $COUNT -eq 1 ]; then
    CHANGE_TYPE=$(awk -F': ' '/^change_type:/ {print $2}' $CHLOG | xargs)
    echo $CHANGE_TYPE
    exit 0
else
    echo "Found multiple changelog files - $CHLOG. Ignoring this change."
    exit 1
fi
