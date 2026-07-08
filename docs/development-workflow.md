# Development Workflow

This document defines the standard iterative workflow for evolving ScoutOS.

## Roles

- **You** define the intent, business problem, and validate the outcome.
- **ChatGPT** translates intent into architecture, requirements, acceptance criteria, and reviews implementation.
- **GitHub** stores the shared contract (issues, documentation, architecture, roadmap).
- **Codex** implements the agreed scope.
- **Local execution** validates behavior against real-world scenarios.

## Standard Flow

1. Define the objective.
2. Capture it in GitHub (Issue or documentation).
3. Keep the scope intentionally small.
4. Let Codex implement only the agreed scope.
5. Validate locally.
6. Review against the original acceptance criteria.
7. Commit and push.
8. Close the issue only after successful validation.
9. Capture lessons learned if they change architecture or methodology.

## Guiding Principles

- One vertical slice at a time.
- Prefer working software over speculative abstractions.
- Architecture should emerge from real use cases.
- Every issue should have measurable acceptance criteria.
- Documentation evolves together with implementation.
- Never expand scope during implementation; create a new issue instead.

This workflow should be the default methodology for future ScoutOS evolution.