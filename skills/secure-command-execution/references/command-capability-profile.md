# Command Capability Profile

Use one profile per command family. Keep the profile smaller than the executable's full grammar.

## Required fields
- executable identity or allowed executable set;
- allowed operation/subcommand shapes;
- flags/options allowed per operation and whether values are required;
- positional value types: path, revision, identifier, numeric bound, enum, etc.;
- authorized cwd/root and canonicalization rule;
- stdin shape and maximum size;
- positive child-environment keys plus explicitly forbidden influence variables;
- allowed filesystem/network/process effects;
- timeout/output/resource limits;
- postcondition and rollback/recovery probe;
- redaction rules and observability fields that must remain visible.

## Adversarial profile tests
For every profile, test at least one case from each relevant family: unknown flag/subcommand; flag abbreviation; `--` boundary abuse; path traversal/symlink/cwd escape; Unicode/confusable option markers; config/plugin/hook injection; hostile inherited environment; URL/header/JSON secret embedding; oversized stdin/output; timeout; non-zero exit; and a command that exits zero without producing the required postcondition.

Do not claim the profile safe because a static denylist catches known payloads. The positive grammar must make unmodeled capability unreachable, and the tests must exercise the real process construction path.
