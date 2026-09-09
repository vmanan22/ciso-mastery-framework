#!/usr/bin/env bash
# Native exit status is the gate; SARIF is evidence, not a success signal.
set -euo pipefail

target=${1:-07_PRIMARY_PROJECT/containers/app/}
report=${2:-semgrep.sarif}
if (( $# >= 2 )); then
  shift 2
else
  set --
fi
if (( $# == 0 )); then
  set -- auto 07_PRIMARY_PROJECT/.semgrep.yml
fi
configs=()
for config in "$@"; do
  configs+=(--config "$config")
done
exec semgrep scan --error --strict --severity ERROR \
  "${configs[@]}" --sarif --output "$report" "$target"
