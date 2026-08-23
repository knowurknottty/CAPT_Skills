# Supersession and Retargeting

## Supersession
A PR/layer is superseded only when its intended delta is already represented in the target through another accepted path.

Use multiple forms of evidence where material:
- candidate head is already an ancestor of target;
- changed files are byte/tree equivalent to content already landed;
- `git log other --not candidate` (or equivalent ancestry comparison) shows no unique commits needed from the candidate;
- target diff demonstrates no residual intended delta.

Same title, filename set, or similar patch is not enough. If unique content remains, it is not superseded.

## Retargeting
After predecessor content lands in the target, a child PR can usually be retargeted from predecessor branch → target **without changing branch history** if its branch already descends from the predecessor.

Verify both dimensions:
1. **Ancestry:** Git proves predecessor/target relationship to the child head.
2. **PR metadata:** the PR base names the intended current target and its displayed diff is layer-relative.

If metadata is wrong but ancestry is correct, repair metadata only. If ancestry is wrong, metadata cannot repair it; the branch requires an explicitly authorized restack/rebase strategy and re-verification.

## Concurrent landing
When automation or another actor lands content during integration, fetch and classify the new state. Never repeat a merge just because the original plan said that PR was next.
