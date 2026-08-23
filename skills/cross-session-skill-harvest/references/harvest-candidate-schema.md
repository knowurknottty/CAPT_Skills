# Harvest Candidate Packet

A harvest output is evidence for curation, not a live skill.

Recommended fields:
- `candidate_id`
- `capability_class`
- `proposed_trigger`
- `negative_triggers`
- `supporting_episodes[]` — source identity, date, observed outcome, evidence pointer
- `counterexamples[]`
- `reusable_invariants[]`
- `workflow_pattern[]`
- `failure_recovery[]`
- `verification_pattern[]`
- `intrinsic_dependencies[]`
- `adapter_or_environment_details[]`
- `privacy_redactions[]`
- `suggested_existing_owner`
- `suggested_disposition`
- `confidence`
- `coverage_limits[]`
- `unresolved_questions[]`

## Confidence cues
Raise confidence for independent recurrence, direct observed success/failure evidence, user corrections corroborated by behavior, cross-environment portability, and successful falsification attempts.

Lower confidence for summaries without raw evidence, duplicate reports of the same episode, one-project-only details, unresolved counterexamples, incomplete history coverage, or outcomes that were merely claimed rather than verified.

Do not convert confidence into a fake precision score unless the surrounding system defines and validates such a scale.
