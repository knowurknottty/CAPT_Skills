#!/bin/zsh
set -euo pipefail
ROOT="${0:A:h:h}"
TARGETS=(
  "$HOME/.agents/skills"
  "$HOME/.claude/skills"
  "$HOME/.hermes/skills"
)
SKILLS=(
  inversion-creative-director
  inversion-interface-craft
  inversion-motion-craft
  inversion-creative-critic
)
for target in "${TARGETS[@]}"; do
  mkdir -p "$target"
  for skill in "${SKILLS[@]}"; do
    src="$ROOT/skills/$skill"
    dst="$target/$skill"
    if [[ -e "$dst" || -L "$dst" ]]; then
      rm -rf "$dst"
    fi
    ln -s "$src" "$dst"
  done
done
print "Installed ${#SKILLS[@]} Inversion Labs skills into ${#TARGETS[@]} skill roots."
