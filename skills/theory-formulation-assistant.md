---
name: theory-formulation-assistant
description: "Assists theory development with the nx framework -- x = known variables (evidence-backed), n = unknown possibilities -- cataloging knowns, brainstorming unknowns, mapping how knowns constrain unknowns, and prioritizing hypotheses by impact and testability. Use when assisting in theory formulation."
---

# Theory Formulation Assistant

Assist in theory development using the nx framework: x=known variables, n=unknown possibilities.

## Core Capabilities
- **Framework Application**: Apply nx methodology to structure theoretical exploration
- **Variable Identification**: Distinguish known factors (x) from unknown possibilities (n)
- **Hypothesis Generation**: Generate testable hypotheses from nx configurations
- **Gap Analysis**: Identify missing variables and unexplored combinations
- **Validation Planning**: Design experiments and tests for theoretical claims

## nx Framework
- **x (known)**: Established facts, verified data, accepted principles in the domain
- **n (unknown)**: Hypothetical variables, unexplored dimensions, speculative factors
- **nx Interaction**: How knowns constrain unknowns and unknowns expand knowns
- **Iteration**: Each discovery moves an n to x, revealing new n possibilities

## Workflow
1. Define the domain and articulate the theory being explored
2. Catalog all known variables (x) with supporting evidence
3. Brainstorm unknown possibilities (n) — variables, interactions, edge cases
4. Map nx relationships: which unknowns are constrained by which knowns?
5. Prioritize n variables by impact and testability
6. Design validation approach for highest-priority hypotheses

## Pitfalls
- Don't confuse assumptions with knowns (x requires evidence)
- Avoid infinite n expansion — focus on plausible, impactful unknowns
- Balance rigor with creativity — the framework serves discovery, not constraint

## Inputs

- `domain` + `theory` -- the domain and the theory being explored, articulated up front
- `knowns` (x) -- established facts, verified data, accepted principles, each with supporting evidence
- `unknowns` (n) -- hypothetical variables, unexplored dimensions, edge cases to brainstorm

## Outputs

- An nx map: cataloged knowns, brainstormed unknowns, and their interactions (how knowns constrain unknowns, how unknowns expand knowns)
- Hypotheses prioritized by impact and testability, with a validation/experiment plan for the top ones -- each discovery moves an n to x, revealing new n possibilities

## Example

A pricing theory: x = historical conversion data, price elasticity studies; n = anchoring effects, competitor response, bundle framing -> anchoring prioritized (high impact, testable) -> A/B validation designed.
