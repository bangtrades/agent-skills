# Operations

Read only the relevant section. The entrypoint controls execution budgets, context renewal and dispatch; this reference preserves detailed verification rules.

## Operator-Runbook Execution (orchestrator-performed production changes)

When the operator gates open a runbook (data cutover, credential rotation, infra change), the orchestrator may execute it directly — held to the same standard as a code wave:

- **Discover live state before following the plan.** The plan's dominant risk may have expired: a cutover runbook built around in-flight-run safety was executed in a window where in-flight = 0 because the scheduler had been off for a day — discovered, not scheduled. Conversely a mid-sequence surprise (the fail-closed build deployed *before* its data migration, refusing readiness for 28h) can be benign, self-announcing state rather than an incident — a fail-closed design makes deploy-order mistakes survivable, which is part of why you build them.
- Execute gate by gate, asserting each postcondition in a *separate statement* (data-modifying-CTE snapshots lie about their own effects), recording preflight numbers before the change and comparing after.
- End with the Law 3d ladder: live traffic through the new path, source frozen, and an audit row recording what was done and why.
- Restore ambient state you changed for the probe (re-disable the job you enabled), and say so.
- **Qualify database authority as an exact identity tuple (2026-09-06 cutover).** A successful statement under a similarly named role does not prove production privilege: record and assert the actual LOGIN, role memberships, grantor, admin option, `INHERIT`, active role after `SET ROLE`, security-definer owner/search path, and the expected ACL as set equality; exercise positive and cross-workspace negative controls through the connection path production uses.
- **A deployment proves only the command it ran.** Read back the service's current source, exact commit, Dockerfile, root, start command, healthcheck, variables by name, volume mount and auto-deploy flag before release; a maintenance container or provider `SUCCESS` record is not readiness — acceptance begins when the full production factory boots and its real health endpoint and worker loops prove current behavior. Verify the public domain target against the actual listen port in startup logs (internal health on 8080 while the domain routed to 8000 and returned 502), and compare a monitor's stale threshold with the producer's actual cadence before deploying it. Run probes inside the real production image before claiming they are executable there (a slim image may lack Git); a host-generated commit manifest verifies mounted source only if the verifier checks every blob and exact file-set equality.
- **Keep credential planes separate.** A connector credential, an interactive browser session and a deployable runtime secret are different capabilities — never infer one supplies another, copy OAuth material between them, or place secrets in evidence; provision runtime credentials through the provider secret manager, verify presence without printing values, and test the application seam independently. A live alert-mapping test proves transport and persistence only: pair it with separate authentic control-origin tests, keep occurrence, persistence, delivery, acknowledgement and escalation timestamps distinct, and never let automated operator credentials stand in for human response.


## Detached hermes-agent Fleets (mechanics earned 2026-08-22/23)

- **Budget is finite and invisible:** `hermes chat -q` defaults to ~90 tool iterations — long slices die mid-flight *without reports*. Pass `--max-turns` sized to slice scope at launch, and resume dead sessions (`--resume <id>`) rather than redispatching: resumed context beats a cold restart.
- **Namespace runtime artifacts per sprint, and assert before spawn:** a launcher pointing Track B at last sprint's same-named brief cost a full false-start wave (the agent diligently worked the WRONG queue). Launcher asserts `[ -f "$BRIEF" ] || exit 2`; report paths carry the sprint suffix too.
- **Harness-tracked background watchers get reaped (SIGTERM); nohup+disown agents survive.** Don't arm fire-and-forget watchers — poll inline in foreground windows (sleep loops ≤600s per call), or you learn nothing when the monitor itself dies silently.
- **A shared checkout makes mid-wave suite runs LIE.** Another track's concurrent `tsc` swaps `dist/` under a running suite → phantom reds that vanish on a quiet tree (four phantom failures burned a diagnosis cycle this way; a zombie build-poll loop was the culprit — kill it, it burns budgets AND poisons verification). Certification requires the graded tree, shared build outputs, and relevant processes to be quiet; unrelated agents working on disjoint outputs need not stop.
- **Board discipline stays operator-shaped:** In Progress at dispatch (batch save), evidence comments at completion, In Review on verified-done, never Done. Verify each state change with a filtered re-list, not trust of save responses.


## Sandboxed-Shell Environments

- **Backgrounded processes do not outlive the call that started them** where each shell invocation runs in its own `bwrap --unshare-pid --die-with-parent` namespace. A server started in one call is gone by the next; on-disk state (data directories, extracted binaries) persists. Bootstrap scripts must be idempotent and re-run inside every call that needs the service, and any agent handed a connection string must be told this.
- **Root is often unavailable.** `apt-get install` fails; `apt-get download` plus `dpkg -x <deb> <prefix>` gives a working install rootlessly. Set `PATH` and `LD_LIBRARY_PATH` to the prefix and use a socket directory you own.
- **`unlink` may be blocked** in mounted user folders until delete permission is granted; write to new filenames rather than replacing in place, or request the permission explicitly.
- **Before freeing space under `/tmp`, list what the remaining gates need** (`CHROME_PATH`, browsers, caches): a deleted Chromium cache left a Lighthouse target unverified (2026-09-16). Decide the preview path before promising an artifact — in Cowork the first Artifact publish needs an approval card the session cannot show. Parallel Agent dispatch requires every invocation in one message. A session without vault filesystem access delivers a package + `PATCHES.md` (copy commands, index/log lines, verify steps) rather than claiming vault writes.

- **Give mutable verification fixtures an owner.** Agents testing the same preview server must use disjoint dates/accounts/records or separate data roots. Reserve shared browser fixtures explicitly; otherwise a legitimate compare-and-swap conflict can be mistaken for an autosave defect. Record intentional competing-client tests separately from incidental tester interference.

