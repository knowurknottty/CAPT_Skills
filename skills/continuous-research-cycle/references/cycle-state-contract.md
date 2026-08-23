# Cycle State Contract

A continuous-research checkpoint must make the next cycle reconstructable without rereading the whole corpus.

## Minimum checkpoint
- corpus/workspace identity and current schema/version signal;
- cycle ID plus time/date boundary derived from live state;
- prior checkpoint/artifact identity used as input;
- active threads with status and last material evidence date;
- inherited priorities and disposition this cycle;
- findings added, corrected, weakened, retired, or left unchanged;
- honest gaps / blocked questions;
- marginal-value verdict;
- exact next-cycle priorities and their evidence dependency.

## Interrupted-cycle recovery
If machine-readable evidence exists for cycle N but synthesis/log/handoff does not, treat N as interrupted rather than allocating N+1. Preserve the orphaned evidence, determine the intended assignment from the previous checkpoint, check integrity locally, then refresh only the load-bearing external evidence needed to establish currency. Complete N or mark it explicitly abandoned before advancing the sequence.

## Schema drift
Fingerprint one or more recent artifacts before writing. A current corpus's actual keys/status values outrank an old reference template. When migration is intentional, record the boundary and do not rewrite historical artifacts merely to make all cycles look uniform.
