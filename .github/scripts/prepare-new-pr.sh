#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# This script uses chloggen file to get the change_type and adds it as a label to the PR.
# If there are none or multiple changelog files, it will ignore the PR.
#
# Notes:
#  - label should exist in the repository in order to add it to the PR.
#  - if label already exist, this is a no-op.
#  - if any error happens, the script quietly exits with 0.

if [ -z ${PR:-} ]; then
    echo "PR number is required"
    exit 1
fi

if [ -z ${PR_CHANGELOG_PATH:-} ]; then
    echo "PR_CHANGELOG_PATH is required"
    exit 1
fi

CHLOG="$(gh pr view $PR --json files --jq '.files.[].path | select (. | startswith(".chloggen/"))')"
echo "Change log file(s): ${CHLOG}"

if [ -z "$CHLOG" ]; then
    echo "No changelog found in the PR. Ignoring this change."
    exit 0
fi

COUNT="$(echo "$CHLOG" | wc -l)"
if [ $COUNT -eq 1 ]; then
    CHANGE_TYPE=$(awk -F': ' '/^change_type:/ {print $2}' "$PR_CHANGELOG_PATH/$CHLOG" | xargs)
    echo $CHANGE_TYPE
    gh pr edit "${PR}" --add-label "${CHANGE_TYPE}" || true
    AREA=$(awk -F': ' '/^component:/ {print $2}' "$PR_CHANGELOG_PATH/$CHLOG" | xargs)
    echo $AREA
    if [[ "$AREA" == \[*\] ]]; then
      cleaned=$(echo "$AREA" | tr -d '[]' | tr ',' '\n')
    else
      cleaned="$AREA"
    fi
    for item in $(echo "$cleaned" | tr ',' ' '); do
      gh pr edit "${PR}" --add-label "area:${item}" || true
    done
else
    echo "Found multiple changelog files. Ignoring this change."
fi
