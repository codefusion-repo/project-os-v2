# Auditar Adaptadores en Target

OPERATION:
  Resolve codefusion-repo/project-os-v2 for actor.browser_chat, workflow.review_only, mode.review_only.
  A terminal agent may run the read-only auditor (tools.audit_target_adapters) against a local target checkout.

INPUT:
  TARGET_REPOSITORY=<TARGET_REPOSITORY>

KERNEL:
  Resolve kernel/manifest.json. Follow resolution_sequence exactly.
  Fail closed if the target adapter state cannot be read.

LIVE_STATE:
  Read the target adapters and adoption docs live (AGENTS.md and any adoption files under the target).
  Compare the current adapter against this repository's canonical model.

DO:
  Detect drift or invasive modifications versus the canonical adapters/*.target.md.
  Report structural failures and drift with evidence references.

OUTPUT:
  output.status_result with a read-only drift report.

LIMITS:
  Read-only audit; applies no fixes. Repairing drift is the upgrade operation, not this one.


RECOMMENDED_NEXT_OPERATION:
  If drift found, Operation 23 (Upgrade kernel adoption) or manual correction.
