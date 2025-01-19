#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
#

if [ -z ${PR:-} ]; then
    echo "PR number is required"
    exit 1
fi

# set -o xtrace

CHLOG="$(gh pr view $PR --json files --jq '.files.[].path | select (. | startswith(".chloggen/"))')"
echo "Change log file: ${CHLOG}"

COUNT="$(echo "$CHLOG" | wc -l)"
if [ -z "$CHLOG" ]; then
    echo "No changelog found in the PR. Ignoring this change."
    exit 0
fi

if [ $COUNT -eq 1 ]; then
    CHANGE_TYPE=$(awk -F': ' '/^change_type:/ {print $2}' $CHLOG | xargs)
    echo $CHANGE_TYPE
    gh pr edit "${PR}" --add-label "${CHANGE_TYPE}" || true
else
    echo "Found multiple changelogs - $CHLOG. Ignoring this change."
fi

exit 0
