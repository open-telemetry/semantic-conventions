#!/usr/bin/env bash
#
# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0
#
# Get a list of the semantic conventions areas from the registry.

CUR_DIRECTORY=$(dirname "$0")
REPO_DIR="$( cd "$CUR_DIRECTORY/../../../" && pwd )"
REGISTRY_DIR="$( cd "$REPO_DIR/model/registry" && pwd )"


for entry in $(ls $REGISTRY_DIR | egrep '\.yaml$' | sort)
do
  echo "$entry"
done
