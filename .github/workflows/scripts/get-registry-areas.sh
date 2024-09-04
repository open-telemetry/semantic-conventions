#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# Get a list of the semantic conventions areas from the registry.

CUR_DIRECTORY=$(dirname "$0")
REPO_DIR="$( cd "$CUR_DIRECTORY/../../../" && pwd )"
REGISTRY_DIR="$( cd "$REPO_DIR/model/registry" && pwd )"

# Explicitly sort with `-d` (dictionary) so BSD and GNU work alike.
for entry in $(ls $REGISTRY_DIR | egrep '\.yaml$' | sort -d)
do
  echo "$entry"
done
