---
name: deep-research
description: >
  Use when one bounded investigation needs comprehensive multi-thread evidence gathering,
  contradiction testing, source provenance, uncertainty accounting, and an evidence-complete synthesis.
version: 2.0.0
metadata:
  author: Inversion Labs
  role: bounded-evidence-synthesis
---

# Deep Research

## Use when
- The user asks for a comprehensive/deep investigation rather than a lookup.
- The question spans multiple subclaims, disciplines, source types, or competing explanations.
- A decision/report must show how claims trace to sources and where uncertainty remains.
- Superficial breadth would hide important contradictions, provenance, or causal structure.

## Do not use when
- One fact or narrow comparison can be answered directly.
- Research must persist across recurring runs; use `continuous-research-cycle`.
- The task is only to format already-supplied material; no new investigation is needed.
- The scope is unbounded enough that no completion criteria can be stated; define the research boundary first.

## Authority and scope
Own **research-question decomposition, source strategy, claim/evidence mapping, contradiction search, coverage/saturation judgment, and synthesis**. Do not convert user assertions, search snippets, model suggestions, or source reputation into facts without supporting evidence. Do not suppress material contrary evidence to make a cleaner narrative.

“Comprehensive” means the stated research threads and material alternatives reached an evidence/gap disposition—not that every document on the topic was found.

## Workflow
1. **Define the research contract.** State the central question, required deliverable, time/currentness boundary, audience, exclusions, and what would count as sufficient evidence. Turn vague “everything” requests into explicit coverage axes without discarding user-named threads.
2. **Build a question map.** Decompose the topic into answerable subquestions, candidate explanations, dependencies, and known unknowns. Separate factual, historical, quantitative, causal, normative, and predictive claims because they require different evidence.
3. **Plan source acquisition.** Identify the best source class per subclaim. Prefer original/primary records for load-bearing factual claims; use rigorous secondary synthesis for discovery, context, and fields where no single primary source can answer the question. See `references/source-and-claim-matrix.md`.
4. **Search broad, then follow evidence deep.** Use independent query angles, terminology variants, cited references, names/identifiers, and backward/forward citation chains. A search snippet can discover a source; it is not a substitute for reading the source when the conclusion depends on details absent from the snippet.
5. **Atomize claims.** Record the specific claim, supporting source/location, date/version, evidence class, and confidence. Keep quotation, paraphrase, calculation, and inference distinguishable. Never let one citation float over a paragraph of unrelated claims.
6. **Run a contradiction/falsification pass.** Search deliberately for contrary evidence, alternate definitions, changed versions, negative/null results, methodological criticism, and explanations that fit the same observations. Preserve disagreements rather than averaging them away.
7. **Check thread saturation.** For each research thread, require at least one substantive source path, a contradiction/alternative check, and an explicit gap disposition. Continue where new searches still change material conclusions; stop expanding threads that only repeat known evidence.
8. **Synthesize across threads carefully.** Connect findings only when evidence supports the relationship. Label causal, correlational, chronological, structural, and speculative connections differently. Derived calculations show inputs and assumptions.
9. **Surface uncertainty and novel deductions.** State what is VERIFIED/CORROBORATED, INFERRED, CONTESTED, or UNVERIFIED. Novel insights are welcome only when the reasoning chain is shown and are not presented as sourced facts.
10. **Deliver in the requested medium.** Use the user's requested report/site/table/document format. Preserve source links/identifiers, material counterevidence, methods, unresolved questions, and the boundary of what was actually researched.

## Failure and recovery
If an extraction path fails, change acquisition strategy or downgrade what can be claimed; do not repeatedly invoke a known-broken path. If a key source is inaccessible, seek an authoritative mirror/citation trail and mark the original evidence gap. If sources conflict, diagnose date/version/population/definition/method differences before declaring one wrong. If the scope exceeds available time/tools, preserve the question map and report which threads are complete versus partial.

## Evidence required
Retain the research contract, question map, source identities, claim/evidence matrix, material contradictions, calculations/assumptions, coverage status per thread, and unresolved gaps. Citations support only the claims they actually evidence.

## Stop conditions
STOP when the research contract's coverage criteria are met and additional searching no longer changes material conclusions, or when a blocker prevents a required evidence class from being obtained. Do not claim exhaustive/comprehensive completion while a named core thread lacks a source/gap disposition or while material contrary evidence remains unreconciled.

Load `references/source-and-claim-matrix.md` for source hierarchy, claim status, and saturation criteria.
