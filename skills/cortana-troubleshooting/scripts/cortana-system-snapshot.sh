#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"

if [[ "${ROOT_DIR}" != "/Users/nolan/Cortana/platform" ]]; then
  printf 'WARN  expected root /Users/nolan/Cortana/platform, got %s\n' "${ROOT_DIR}" >&2
fi

cd "${ROOT_DIR}" || exit 1

section() {
  printf '\n== %s ==\n' "$1"
}

run() {
  printf '$ %s\n' "$*"
  "$@" 2>&1 || printf 'WARN  command failed: %s\n' "$*"
}

curl_json() {
  local url="$1"
  printf '$ curl -fsS %s\n' "${url}"
  if body="$(curl -fsS --max-time 3 "${url}" 2>/dev/null)"; then
    python3 -c 'import json,sys; print(json.dumps(json.load(sys.stdin), indent=2, sort_keys=True))' <<<"${body}" 2>/dev/null || printf '%s\n' "${body}"
  else
    printf 'WARN  endpoint unavailable: %s\n' "${url}"
  fi
}

psql_read() {
  local sql="$1"
  if docker ps --format '{{.Names}}' | grep -qx 'cortana-postgres'; then
    docker exec cortana-postgres psql -U cortana -d cortana -c "${sql}" 2>&1 || true
  else
    printf 'WARN  cortana-postgres container not running\n'
  fi
}

section "Cortana Snapshot"
printf 'root=%s\n' "${ROOT_DIR}"
date -u '+utc=%Y-%m-%dT%H:%M:%SZ'

section "Git"
run git status --short

section "Docker Services"
if command -v docker >/dev/null 2>&1; then
  run docker ps --filter name=cortana --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
else
  printf 'WARN  docker not found in PATH\n'
fi

section "HTTP Health"
curl_json "http://127.0.0.1:4400/healthz"
curl_json "http://127.0.0.1:4400/readyz"
curl_json "http://127.0.0.1:4200/api/health"

section "Recent Agents"
psql_read "select id, name, adapter_type, status, updated_at from agents order by updated_at desc limit 10;"

section "Recent Issues"
psql_read "select id, identifier, title, status, updated_at from issues order by updated_at desc limit 10;"

section "Recent Heartbeat Runs"
psql_read "select id, agent_id, invocation_source, status, started_at, finished_at from heartbeat_runs order by created_at desc limit 10;"

section "Recent Router Ledger"
psql_read "select agent_id, provider, model, cost_usd, ts from llm_cost_ledger order by ts desc limit 10;"

section "Recent Activity Log"
psql_read "select action, entity_type, agent_id, created_at from activity_log order by created_at desc limit 10;"

section "Verifier Availability"
for script in \
  scripts/healthcheck.sh \
  scripts/verify-cortana.sh \
  scripts/verify-s10d-9-router-ui-budget.sh \
  scripts/cortana-router-smoke-real.sh
do
  if [[ -x "${script}" ]]; then
    printf 'OK    executable %s\n' "${script}"
  elif [[ -f "${script}" ]]; then
    printf 'WARN  present but not executable %s\n' "${script}"
  else
    printf 'WARN  missing %s\n' "${script}"
  fi
done

section "Documents Path Guard"
scan_targets=(
  "docker-compose.yml"
  "config"
  "containers"
  "scripts"
  "tests"
  "workspaces/cortana-adapters"
  "workspaces/paperclip/server"
  "workspaces/paperclip/ui"
)
if rg -n --hidden --glob '!node_modules/**' --glob '!.git/**' --glob '!data/**' --glob '!state/**' '/Users/[Nn]olan/Documents/' "${scan_targets[@]}" 2>/dev/null | grep -F -v 'Documents/...' >/tmp/cortana-documents-refs.txt; then
  printf 'WARN  possible Documents subpath references found; inspect before enabling agents:\n'
  sed -n '1,40p' /tmp/cortana-documents-refs.txt
else
  guard_count="$(rg -n --hidden --glob '!node_modules/**' --glob '!.git/**' --glob '!data/**' --glob '!state/**' '/Users/[Nn]olan/Documents|/Users/Nolan/Documents' "${scan_targets[@]}" 2>/dev/null | wc -l | tr -d ' ')"
  printf 'OK    no Documents subpath usage found in scanned source/config files (policy guard references=%s)\n' "${guard_count:-0}"
fi

section "Notes"
printf 'This snapshot is read-only. It does not mutate Docker, Postgres, markers, credentials, issues, runs, or agents.\n'
