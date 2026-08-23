# Worktree and Stash Preservation

Before deleting a worktree, temporary clone, branch, or stash, determine whether it contains the only copy of work.

## Worktree check
- Record worktree path and HEAD.
- Test whether HEAD is reachable from a surviving ref (`git branch --all --contains <sha>` or equivalent).
- Inspect staged, unstaged, and untracked state inside that worktree.
- Reachable + clean supports removal; unreachable or dirty requires preservation first.

Do not infer safety from a detached HEAD alone. Detached is a checkout state, not evidence that work is orphaned or redundant.

## Stash check
- Enumerate stashes before operations that may re-clone, rewrite, or remove repositories.
- Record each stash base/identity and export its patch/content when it is not otherwise preserved.
- Remember that stashes survive many local operations but are not transported by a fresh clone.

## Unreachable objects
Read object type, not just count. Unreachable blobs commonly represent churn; an unreachable commit may contain unique history.

## Preservation rule
When uniqueness is uncertain, preserve SHA + diff/patch + untracked artifacts to an explicit evidence location before cleanup. Do not call content “backed up” until the preserved copy is independently readable.
