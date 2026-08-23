# Construction and Equivalence Gates

## Before construction
- Source `BASE`/`HEAD` and manifest are frozen.
- Source CI is terminal and any red result classified.
- Every path/hunk has one owner.
- Required-CI cross-scope couplings are resolved.
- Rewrite/no-rewrite choice is explicitly authorized.

## Per branch
1. Start from the exact predecessor HEAD.
2. Apply only owned files/hunks from the frozen source candidate.
3. Verify diff/path set against the manifest before commit.
4. Run the checks required for that scope and inherited baseline.
5. Push first and confirm the remote ref points to the expected HEAD.
6. Create/update the PR with the immediate predecessor as base.
7. Confirm remote CI belongs to that exact head SHA and completes successfully.

## Final stack
For every adjacent pair:
- prove predecessor is an ancestor of successor;
- verify PR metadata base is the immediate predecessor, not merely some ancestor;
- verify remote PR head SHA equals the expected branch SHA.

Then compare terminal stack output/tree against the frozen source candidate. Exact equivalence is strongest. If the stack intentionally differs, maintain an explicit allowlist with semantic justification and independent verification for every difference.

Do not repair a metadata-only PR-base error by rewriting healthy branch history. Do not repair wrong ancestry by editing PR metadata alone.
