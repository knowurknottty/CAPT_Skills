# Relationship and Provenance Contract

## Relationship semantics
Do not validate all edges as one graph. Define each relation's target type and invariants.
- dependency / extends / supersedes / derived-from: usually ID references; acyclicity may be required by semantics;
- integrates-with / related-to / optional-with: ID references where cycles may be legitimate;
- conflicts-with: ID reference with symmetry validation;
- provides / capabilities / labels: may be free-form values rather than record IDs.

Validate target existence only for relations whose contract says the target is an ID. A blanket DAG rule produces false modeling when mutual integration is legitimate.

## Field-level provenance
For material fields that can drift, record enough to answer: who/what asserted this, how strong is the evidence, when/version was it checked, and when should it be refreshed. A minimal shape may include `source`, `authority`, `status` (`verified|inferred|curated|needs-confirmation`), `verified_at` or source revision, and `refresh_policy`.

Provenance does not make weak data strong; it makes weakness visible and machine-actionable.
