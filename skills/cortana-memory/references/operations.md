# Memory Pillar Operations

Operator and agent ceremonies for the memory pillar. Every ceremony has preconditions, the canonical script invocation, post-conditions, and a rollback path. Never hand-edit marker files.

## Approval lifecycle

The memory pillar has TWO approval markers per backend. Both ride on the operator-intent contract:

1. **Read marker** — `state/cortana-memory/live-dispatch-approved.marker`
2. **Write marker** — `state/cortana-memory/live-write-approved.marker` (requires the read marker to exist for the same agent first)

All ceremonies go through `scripts/cortana-memory-live-approval.sh`. The script enforces:
- Refuse without `--yes` (or `--approved` / `--operator-approval`)
- Refuse outside `/Users/nolan/Cortana/platform` working root
- Refuse if a backup file already exists for the same run-ts (when applicable)
- For write grants: refuse if `--ceremony-acknowledged` missing
- For write grants: refuse if `expires_at > paired_canonical_expires_at` of the read marker

### Subcommands

```
cortana-memory-live-approval.sh status | show | inspect | approval-status
cortana-memory-live-approval.sh plan | approval-plan
cortana-memory-live-approval.sh grant | enable | create | approval-grant
   --extension-id <id> --agent-id <uuid>
   [--operator-intent "<reason>"]
   --yes

cortana-memory-live-approval.sh rescind | revoke | delete | remove | approval-rescind
   --extension-id <id>
   --yes

cortana-memory-live-approval.sh grant-write | approval-grant-write
   --extension-id <id>
   --agent-id <uuid>
   --expires-hours <n>                        (≤ remaining life of paired read marker)
   --paired-canonical-expires-at <iso-utc>    (the read marker's expires_at)
   --write-path <glob> [--write-path <glob> ...]
   --operator-intent "<reason>"
   --ceremony-acknowledged
   --yes

cortana-memory-live-approval.sh rescind-write | approval-rescind-write
   --extension-id <id>
   --agent-id <uuid>
   --yes

cortana-memory-live-approval.sh migrate | approval-migrate
   (rare; for marker schema migrations)
```

## Ceremony: grant read approval

**Preconditions**:
- Operator confirms agent identity and scope
- Backend (`para-memory-files`) is registered
- Agent exists in `agents` table

**Steps**:

```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-memory-live-approval.sh grant \
  --extension-id para-memory-files \
  --agent-id <agent-uuid> \
  --operator-intent "<reason>" \
  --yes
```

**Post-conditions**:
- `state/cortana-memory/live-dispatch-approved.marker` updated
- Agent UUID now in `agent_ids[]`
- `expires_at` set (default TTL per ceremony policy)
- Audit emission resumes (subsequent dispatches show `audit_category=live_<op>_success` instead of `refused_marker_*`)

**Rollback**: `rescind` subcommand removes the agent from `agent_ids[]` (or removes the file when last agent is rescinded).

## Ceremony: grant write approval

**Preconditions**:
- Read marker exists, unexpired, agent UUID in `agent_ids[]`
- Operator has read the write-ceremony risk language
- The required `--write-path` globs cover the agent's intended targets

**Steps**:

```bash
# Find the paired read marker's expiry first
READ_EXP=$(cat /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker | jq -r '.expires_at')

# Compute hours remaining (must be ≥ the --expires-hours value)
# (use date math; see scripts/cortana-memory-live-approval.sh for the exact computation)

bash /Users/nolan/Cortana/platform/scripts/cortana-memory-live-approval.sh grant-write \
  --extension-id para-memory-files \
  --agent-id <agent-uuid> \
  --expires-hours <n>                    # ≤ remaining hours on read marker
  --paired-canonical-expires-at "$READ_EXP" \
  --write-path "smoke/**" \
  --write-path "operator-tests/**" \
  --operator-intent "<reason>" \
  --ceremony-acknowledged \
  --yes
```

**Post-conditions**:
- `state/cortana-memory/live-write-approved.marker` updated with `agent_id`, `write_paths_allowlist[]`, `expires_at`, `paired_canonical_expires_at`, `ceremony_acknowledged: true`
- Writes to allowlisted paths now allowed; `audit_category=live_write_success` on dispatch

**Rollback**: `rescind-write` subcommand removes the agent from the write marker (or deletes the file when last agent is rescinded).

## Ceremony: inspect approvals

```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-memory-live-approval.sh status \
  --extension-id para-memory-files

# Or direct inspection:
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker | jq '.'
cat /Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker  | jq '.'
```

**Healthy state for an active agent**:
- Read marker `expires_at` in the future, agent UUID in `agent_ids[]`
- Write marker `expires_at` ≤ read marker `expires_at`, `paired_canonical_expires_at` matches, `agent_id` set, `write_paths_allowlist[]` covers intended scope, `ceremony_acknowledged: true`

## Capability marker management

Capability markers live at `state/agents/<agent-uuid>/capabilities/<cap>.marker`. Each is a JSON file with `capability`, `granted_at`, `granted_by`, optional `expires_at`.

### Inspect capabilities for an agent

```bash
AGENT=<uuid>
ls -la /Users/nolan/Cortana/platform/state/agents/${AGENT}/capabilities/
for f in /Users/nolan/Cortana/platform/state/agents/${AGENT}/capabilities/*.marker; do
  echo "=== $(basename $f) ==="
  cat "$f" | jq '.'
done
```

### Grant a capability

Use the capability ceremony script (or manual write through the operator-approved path; never hand-edit in production):

```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-capability.sh grant \
  --agent-id <uuid> \
  --capability memory_para_files_read \
  --granted-by <operator> \
  --yes
```

Repeat for `memory_para_files_write` if write is needed.

### Revoke a capability

```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-capability.sh revoke \
  --agent-id <uuid> \
  --capability memory_para_files_write \
  --yes
```

## Migrating an agent's memory transport

**Use case**: Move a stateful agent from `cortana_llm_router` (router_tool_loop transport) to `claude_local` (native_cli_bridge transport).

**Preconditions**:
- Agent's UUID is preserved
- Read marker is agent-UUID-keyed (NOT adapter-keyed); confirms `agent_ids[]` contains the UUID
- Write marker is agent-UUID-keyed; same check
- Capability markers under `state/agents/<uuid>/capabilities/` are intact

**Steps**:

```bash
# 1. Pre-flight: marker integrity check (the migration script does this automatically; do it manually first as a sanity)
AGENT=<uuid>
jq -r --arg a "$AGENT" \
   '.agent_ids[] | select(. == $a) | "PRESENT_IN_READ_MARKER"' \
   /Users/nolan/Cortana/platform/state/cortana-memory/live-dispatch-approved.marker
jq -r --arg a "$AGENT" \
   'select(.agent_id == $a or (.agent_ids // []) | index($a)) | "PRESENT_IN_WRITE_MARKER"' \
   /Users/nolan/Cortana/platform/state/cortana-memory/live-write-approved.marker

# 2. Dry-run the migration
bash /Users/nolan/Cortana/platform/scripts/cortana-agent-migrate-symba-to-claude-local.sh

# 3. Execute
bash /Users/nolan/Cortana/platform/scripts/cortana-agent-migrate-symba-to-claude-local.sh --yes

# 4. Verify post-migration row
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, adapter_type,
          adapter_config->'memoryBridge'->>'transport' AS transport,
          adapter_config->'mcp_servers'->'cortana-memory'->'env'->>'CORTANA_AGENT_ID' AS mcp_agent_id
     FROM agents WHERE id='${AGENT}'"
```

**Post-conditions**:
- Postgres `agents.adapter_type=claude_local`
- `adapter_config.memoryBridge.transport=mcp` (adapter-side label)
- Future audit rows for this agent show `transport=native_cli_bridge`
- Read + write markers unchanged (agent-UUID-keyed)

**Rollback**:
```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-agent-migrate-symba-to-claude-local.sh \
  --rollback state/migrations/symba-pre-claude-local-<UTC>.json \
  --yes
```

## Candidate promotion ceremony (STEP-44)

Agents submit candidate files via `cortana_memory_submit_candidate`. The classifier runs against `config/cortana/memory-promotion-rules.json` and emits one of:

- `candidate_submit_accepted` → file lives under `state/cortana-memory/candidates/<agent-id>/`
- `candidate_promotion_auto_approved` → file copied to `state/cortana-memory/shared/<sub-tree>/` automatically
- `candidate_promotion_escalated` → operator must approve manually

### Operator-approved promotion

For escalated candidates:

```bash
# 1. List pending candidates
ls -la /Users/nolan/Cortana/platform/state/cortana-memory/candidates/<agent-id>/

# 2. Inspect the candidate file
cat /Users/nolan/Cortana/platform/state/cortana-memory/candidates/<agent-id>/<path>

# 3. Approve via the promotion ceremony script
bash /Users/nolan/Cortana/platform/scripts/cortana-memory-promote-candidate.sh \
  --agent-id <agent-uuid> \
  --relative-path <path> \
  --target shared/<sub-tree>/<path> \
  --operator-intent "<reason>" \
  --yes
```

**Post-conditions**:
- File appears under `state/cortana-memory/shared/<sub-tree>/<path>`
- Audit row stamped with `audit_category=candidate_promotion_completed`
- Candidate file removed from `candidates/<agent-id>/`

### Rejecting a candidate

```bash
bash /Users/nolan/Cortana/platform/scripts/cortana-memory-promote-candidate.sh \
  --agent-id <agent-uuid> \
  --relative-path <path> \
  --reject \
  --operator-intent "<reason>" \
  --yes
```

## Cleanup ceremonies

### Sweep stale revoked board_api_keys (memory pillar adjacent)

```bash
# Read-only inspection first
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, name, revoked_at
     FROM board_api_keys
    WHERE revoked_at IS NOT NULL
      AND revoked_at < NOW() - INTERVAL '7 days'"

# Delete one specific row (the auto-mode classifier may refuse bulk deletes)
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "DELETE FROM board_api_keys
    WHERE id='<specific-uuid>'
      AND revoked_at IS NOT NULL
      AND revoked_at < NOW() - INTERVAL '7 days'"
```

### Retire orphan wakeup_request rows

```bash
# Inspect first
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "SELECT id, agent_id, source, requested_at
     FROM agent_wakeup_requests
    WHERE status='queued'
      AND requested_at < NOW() - INTERVAL '1 hour'
    ORDER BY requested_at DESC"

# Retire a specific orphan
docker exec cortana-postgres psql -X -U cortana -d cortana -c \
  "UPDATE agent_wakeup_requests
      SET status='skipped',
          finished_at=NOW(),
          error='<reason>'
    WHERE id='<specific-uuid>' AND status='queued'"
```

### Prune old smoke artifacts in agent vault scopes

Agents own their private scope; the operator may prune stale smoke artifacts during pillar hygiene:

```bash
AGENT=<uuid>
find /Users/nolan/Cortana/platform/state/cortana-memory/${AGENT}/smoke/ \
  -name "*.md" -mtime +30 -type f
# review the list; then:
find /Users/nolan/Cortana/platform/state/cortana-memory/${AGENT}/smoke/ \
  -name "*.md" -mtime +30 -type f -delete
```

Never prune `shared/`, `glossary/`, `core/`, `projects/`, or `workflows/` without a promotion-classifier audit first.

## Verification gates

| Gate | Path | Purpose | Run frequency |
| --- | --- | --- | --- |
| `verify-s10i-4-native-cli-memory-bridge.sh` | scripts/ | Static + runtime native bridge readiness | Pre-flight before any memory work |
| `verify-s10i-6-controlled-codex-memory-smoke.sh` | scripts/ | Controlled Codex smoke (canonical baseline) | After any platform-level change |
| `verify-s10i-12-native-memory-e2e.sh` | scripts/ | End-to-end native memory bridge | After bridge / MCP changes |
| `verify-s10j-1-memory-adapter-protocol.sh` | scripts/ | Protocol completeness (S10J-1) | When adding a backend |
| `verify-s10j-4-shared-memory-isolation.sh` | scripts/ | Aggregate release gate | Pre-promotion checks |
| `verify-s10j-5-sustained-window.sh` | scripts/ | Sustained-window counter (7-day stability) | Daily |
| `cortana-memory-mcp-status.sh` | scripts/ | MCP bridge runtime probe | When triaging MCP issues |

Run the cross-pillar regression matrix (`canonical-commands.md` §16 in `paperclip-triage`) after every backend swap or transport change.

## Hard rules (operations)

- Never grant a write marker without read marker present and agent-listed
- Never grant a write marker with `expires_at > paired_canonical_expires_at` of the read marker (the script enforces; this is a defense-in-depth reminder)
- Never write `--ceremony-acknowledged` without actually reading the write-ceremony risk language
- Triage tokens (board_api_keys) MUST be revoked at the end of each triage slice
- Promotion rules can be edited only via the rules-versioning ceremony (bump v1 → v2); never silently edit
- Capability grants for `*_write` go through the same write-ceremony cadence as marker grants
- A backend swap is NEVER a single-step operation; always follow the swap drill in `upgrade-ceremony.md`
