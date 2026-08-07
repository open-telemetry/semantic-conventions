#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$SCRIPT_DIR/../.."

cd "$ROOT_DIR"

targets=()
if [[ $# -gt 0 ]]; then
  targets=("$@")
else
  while IFS= read -r -d '' target; do
    targets+=("$target")
  done < <(git ls-files -z -- '*.md' '*.yaml' '*.yml')
fi

if [[ ${#targets[@]} -eq 0 ]]; then
  echo "No files to check for OpenTelemetry specification redirects."
  exit 0
fi

urls=()
while IFS= read -r url; do
  [[ -n $url ]] && urls+=("$url")
done < <(
  grep -hEo \
      "https://opentelemetry\\.io/docs/specs/otel/[^][[:space:]<>()\"']*" \
      "${targets[@]}" |
      sed -E 's/[.,;:]+$//; s/#.*$//' |
      sort -u
)

failures=0
for url in "${urls[@]}"; do
  if ! response=$(curl \
    --head \
    --silent \
    --show-error \
    --output /dev/null \
    --write-out $'%{http_code}\t%{redirect_url}' \
    --connect-timeout 10 \
    --max-time 30 \
    --retry 3 \
    "$url"); then
    echo "Unable to check OpenTelemetry specification link: $url" >&2
    failures=$((failures + 1))
    continue
  fi

  IFS=$'\t' read -r status redirect_url <<< "$response"
  if [[ $status =~ ^3[0-9][0-9]$ ]]; then
    echo "Redirecting OpenTelemetry specification link: $url" >&2
    echo "  $status -> $redirect_url" >&2
    failures=$((failures + 1))
  fi
done

if [[ $failures -gt 0 ]]; then
  echo "Found $failures redirecting or unreachable OpenTelemetry specification link(s)." >&2
  exit 1
fi

echo "OpenTelemetry specification redirect check passed (${#urls[@]} URLs)."
