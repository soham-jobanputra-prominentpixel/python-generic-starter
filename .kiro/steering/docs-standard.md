---
inclusion: fileMatch
fileMatchPattern: ["**/*.md"]
---


**Scope:** Standards for all Markdown documentation in this repository.
**Audience:** Engineers, reviewers, technical writers.


## 1. Core Principle

Write small but meaningful documentation.
Every word must carry weight.

Long documentation creates reading debt.
Keep documents short, context-rich, dense, and correct.

---

## 2. Structural Rules

### 2.1 One Domain per File

Each file must cover a single concern.

Valid examples:

* `api-rest-conventions.md` — REST API standards
* `testing-unit-patterns.md` — Unit testing strategy
* `components-form-validation.md` — Form validation standards

Do not mix:

* API design + deployment
* Testing + security policy
* Architecture + onboarding

If a file exceeds a single conceptual domain, split it.

---

### 2.2 Clear, Predictable Naming

File names must:

* Be lowercase
* Use hyphen-separated words
* Explicitly state scope
* Avoid vague terms like `misc`, `notes`, `stuff`, `guide`

Naming pattern:
`<domain>-<subdomain>-<focus>.md`

Examples:

* `api-authentication-oauth2.md`
* `deployment-kubernetes-rollout.md`
* `architecture-event-driven.md`

---

## 3. Content Standards

### 3.1 Explain Why

Do not document rules without rationale.

Every major decision must include:

* Problem being solved
* Trade-offs considered
* Why this approach was selected

Bad:

> Use PATCH for updates.

Good:

> Use PATCH for partial updates to prevent full resource overwrites and reduce payload size. PUT remains reserved for full replacement semantics.

---

### 3.2 Provide Concrete Examples

Standards must include:

* Code snippets
* Before/after comparisons
* Anti-patterns when relevant

Example format:

**Bad**

```json
{ "name": "test" }
```

**Good**

```json
{
  "name": "test",
  "createdAt": "2026-01-01T00:00:00Z"
}
```

Examples must be minimal but realistic.

---

### 3.3 Dense Linking

Avoid repetition.
Link to canonical sources instead.

If a concept is defined elsewhere:

* Link it
* Do not restate it

Documentation must form a connected graph, not isolated islands.

---

## 4. Security Requirements

Docs are public, Never include:

* API keys
* Secrets
* Tokens
* Real credentials
* Internal URLs with access implications

All examples must use:

* Placeholder domains (`example.com`)
* Redacted tokens (`<API_KEY>`)
* Mock values

Security violations block merge.

---

## 5. Maintenance Policy

Documentation is versioned and reviewed like code.

Required practices:

* Review during sprint planning
* Revalidate references after restructuring
* Require PR review for all documentation changes
* Update docs when architecture changes — not later

Outdated documentation is considered a defect.

---

## 6. Quality Bar

A document is acceptable only if:

* It cannot be shortened without losing meaning.
* It explains intent, not just mechanics.
* It includes at least one concrete example (when applicable).
* It contains no redundant phrasing.
* It is internally consistent and technically accurate.

If it feels long, it is likely wrong.

---

## 7. Non-Goals

Documentation is not:

* Marketing content
* Tutorials for beginners (unless explicitly scoped)
* A dumping ground for ideas
* A transcript of meetings

Capture decisions. Omit noise.

---

## 8. Review Checklist

Before merging:

* Does this file cover exactly one domain?
* Is the filename explicit and scoped?
* Is every rule justified?
* Are examples minimal and correct?
* Are there redundant sentences?
* Are there any secrets?
* Are links valid?

If any answer fails, revise.
