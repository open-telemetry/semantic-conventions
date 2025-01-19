#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
#

# This script extracts the "Area" from the issue body and adds it as a label
# on newly created issues. The area from the issue body comes from
# the "Area" drop-down field in the ISSUE_TEMPLATE, which is auto-generated
# from the files inside model/registry.

# TODO: This script can be later used to also auto-assign the correct code-owner
# once that is implemented.

set -euo pipefail

OS=$(uname | tr '[:upper:]' '[:lower:]')

if [[ "${OS}" == "darwin" ]]; then
  SED="gsed"
else
  SED="sed"
fi

if [[ -z "${ISSUE:-}" || -z "${BODY:-}" || -z "${OPENER:-}" ]]; then
  echo "Missing one of ISSUE, BODY, or OPENER, please ensure all are set."
  exit 0
fi

LABELS="triage:needs-triage,"
AREAS_SECTION_START=$( (echo "${BODY}" | grep -n '### Area(s)' | awk '{ print $1 }' | grep -oE '[0-9]+') || echo '-1' )
BODY_AREAS=""

if [[ "${AREAS_SECTION_START}" != '-1' ]]; then
    BODY_AREAS=$(echo "${BODY}" | "${SED}" -n $((AREAS_SECTION_START+2))p)
fi

for AREA in ${BODY_AREAS}; do
  # Areas are delimited by ', ' and the for loop separates on spaces, so remove the extra comma.
  AREA=${AREA//,/}

  if (( "${#AREA}" > 50 )); then
    echo "'${AREA}' exceeds GitHub's 50-character limit on labels, skipping adding a label"
    continue
  fi

  if [[ -n "${LABELS}" ]]; then
      LABELS+=","
  fi
    LABELS+="${AREA}"
done

if [[ -v BODY_AREAS[@] ]]; then
  echo "The issue was associated with areas:" "${!BODY_AREAS[@]}"
else
  echo "No related areas were given"
fi

if [[ -n "${LABELS}" ]]; then
  # Notes on this call:
  # 1. Labels will be deduplicated by the GitHub CLI.
  # 2. The call to edit the issue will fail if any of the
  #    labels doesn't exist. We can be reasonably sure that
  #    all labels will exist since they come from a known set.
  echo "Adding the following labels: ${LABELS//,/ /}"
  gh issue edit "${ISSUE}" --add-label "${LABELS}" || true
else
  echo "No labels were found to add"
fi
