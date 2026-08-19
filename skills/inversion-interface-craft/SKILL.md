---
name: inversion-interface-craft
description: >
  Use when building, redesigning, or judging an Inversion Labs web or app interface where
  Impeccable and Taste could overlap, especially mixed marketing/product surfaces, premium
  redesigns, experimental UI, dashboards, landing pages, portfolios, or anti-generic frontend work.
version: 0.1.0
metadata:
  author: Inversion Labs
  role: interface-owner
---

# Inversion Interface Craft

## Hard ownership contract

For every interface artifact, write the ownership explicitly as: **Primary owner: `impeccable`**. `taste` is support only. `design-taste-frontend` is conditional support only on its in-scope marketing surfaces. Never write a combined primary such as "Impeccable + Taste" and never promote a support skill to co-owner.

`impeccable` is the **primary owner** for interface implementation and verification. `taste` supplies domain-grounded judgment. `design-taste-frontend` is a conditional marketing specialist, not a universal UI constitution.

Do not duplicate upstream command playbooks or detector rules here; load the current upstream skill and let it own its mechanics.

## Route the surface first

- **Landing, campaign, portfolio, editorial marketing, or marketing redesign:** use `impeccable` + `taste`; load `design-taste-frontend` for its Design Read, three dials, anti-default vocabulary, and redesign heuristics.
- **Dashboard, admin, dense product UI, data table, multi-step workflow, editor, or operator console:** use `impeccable` + `taste`. **Do not load `design-taste-frontend` for that surface**; its own scope excludes these surfaces. Do not smuggle its individual bans, dials, font preferences, density rules, layout rules, or motion rules back in piecemeal. If a similar decision is correct, re-derive it independently from `impeccable`, `taste`, the product domain, or an official design system.
- **Mixed product:** classify each route/surface separately. A product's landing page is Persuade; its console is Operate.

When `design-taste-frontend` participates, its dials are creative inputs. Its universal-looking preflight bans do not override a pinned brief, product truth, accessibility, an official design system, or Impeccable's medium-specific contract.

## Working contract

1. Run the current `impeccable` setup/context flow and inspect incumbent visual truth before changing code.
2. Use `taste` to state the quality bar, audience knowledge, attention budget, and one-sentence spine.
3. Choose the surface mode and preservation level before visual intervention.
4. Apply the Inversion test: identify both the category cliché and the currently fashionable anti-cliché. Choose a third move only if it improves the job of the surface.
5. Commit to one signature move; let navigation, forms, dense data, and recovery states stay legible and conventional where convention carries usability.
6. Build through the current Impeccable playbook. Never fork its implementation recipes here.

## Precedence

Explicit brief/product truth → safety/accessibility/legal → interaction and platform contract → incumbent brand/content constraints → domain-grounded taste → anti-slop heuristics/dials/novelty.

For product UI, task completion and state legibility outrank expressive composition. For marketing, expression may carry more of the product, but claims still require supplied truth.

## Evidence and finish

A finished claim needs evidence appropriate to the surface: real rendered screenshots at shipped device classes, responsive overflow checks, keyboard/focus behavior, loading/error/empty/disabled states, contrast/accessibility checks, real copy/data, working controls, and build/test/performance evidence when the change touches them.

Every completion plan or handoff must end with this explicit **bounded convergence** contract:

**QA:** inspect all shipped device classes together once → batch-fix all observed defects → confirm once → **STOP** unless the fix introduced a new defect or the user changed the brief. Do not replace this with an open-ended "polish until good" instruction.
