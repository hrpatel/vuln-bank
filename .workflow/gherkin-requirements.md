# Gherkin Requirements Guide

**Requirements (from Jira epics/tickets, agents, or specs) should be written in Gherkin.** This guide helps agents and humans produce consistent, executable feature files that can drive BDD-style tests and serve as the single representation of behavior.

---

## Why Gherkin

- **Single format:** Same language for product requirements, acceptance criteria, and executable scenarios.
- **Parseable:** Tools (Cucumber, Behave, etc.) can run scenarios as tests.
- **Readable:** Given/When/Then structure is clear for stakeholders and agents.
- **Traceable:** Scenarios can reference Jira keys, Beads IDs, or GitHub Issues in tags or descriptions.

---

## Gherkin Basics

### Structure

```gherkin
Feature: Short name of the capability or area
  As a [role]
  I want [something]
  So that [outcome]

  [Optional background or context]

  Scenario: Name of the scenario
    Given [precondition]
    And [another precondition]
    When [action]
    Then [observable outcome]
    And [another outcome]

  Scenario: Another scenario
    Given ...
    When ...
    Then ...
```

### Keywords

| Keyword | Purpose |
|---------|--------|
| **Feature** | One per file; groups scenarios. |
| **Scenario** | One concrete example (Given/When/Then). |
| **Scenario Outline** | Template with **Examples** table for multiple rows. |
| **Background** | Steps run before every scenario in the file. |
| **Given** | Precondition / initial state. |
| **When** | Action / event. |
| **Then** | Expected outcome / observation. |
| **And** / **But** | Continue previous step type. |

### Example (vuln-bank style)

```gherkin
Feature: Login rate limiting
  As a security-conscious application
  I want to limit failed login attempts per account
  So that brute-force attacks are mitigated

  Scenario: User is locked after too many failed attempts
    Given the account "alice" has no prior failed logins
    When the user submits an incorrect password for "alice" 5 times within 1 minute
    Then the account "alice" is locked for 15 minutes
    And the next login attempt for "alice" returns "Account temporarily locked"

  Scenario: Lockout resets after cooldown
    Given the account "bob" is currently locked
    And 15 minutes have passed since lockout
    When the user submits the correct password for "bob"
    Then the user is logged in successfully
```

---

## Where to Put Feature Files

- **Suggested location:** `features/` at repo root (or `tests/features/` if tests live under `tests/`).
- **Naming:** One file per feature or area, e.g. `features/login.feature`, `features/transfer.feature`.
- **Convention:** Match file name to the main capability in the Feature title so agents and tools can discover by name.

---

## How Agents Should Generate Gherkin

### From a requirement or ticket (e.g. Jira)

1. **Identify the capability** — One Feature per epic or coherent user goal; one or more Scenarios per acceptance criterion.
2. **Use the template above** — Feature (title + As/I want/So that), then Scenario(s) with Given/When/Then.
3. **One scenario = one path** — Don’t mix multiple outcomes in one scenario; use multiple scenarios or a Scenario Outline with Examples.
4. **Concrete steps** — Steps should be implementable (e.g. “the user submits an incorrect password” not “something bad happens”). Use quotes for concrete data (“alice”, “5 times”).
5. **Add traceability** — In the Feature description or a comment, include the source (e.g. `# Jira: PROJ-123` or `# Beads: bd-xyz`).

### From an informal spec or agent brainstorm

1. **Extract behaviors** — List “when X, then Y” behaviors.
2. **Group under a Feature** — One Feature per cohesive area.
3. **Write scenarios** — One Scenario per behavior; add Given for setup, When for the trigger, Then for the result.
4. **Refine steps** — Make steps unambiguous and testable; avoid vague language.

### Checklist for generated feature files

- [ ] One **Feature** per file with a short, clear title.
- [ ] **As a / I want / So that** filled when the source provides user-story context.
- [ ] **Scenarios** named clearly (e.g. “User is locked after too many failed attempts”).
- [ ] **Given** sets up state; **When** is the action; **Then** is the observable outcome.
- [ ] Steps are concrete (specific roles, values, and actions).
- [ ] Optional **Scenario Outline** + **Examples** when the same flow applies to multiple inputs.
- [ ] Traceability comment (Jira key, Beads ID, or issue) when applicable.

---

## Linking to Beads and Jira

- **In the file:** Add a comment line at the top or under the Feature, e.g. `# PROJ-456` or `# bd-a1b2`.
- **In Beads:** Use `--acceptance` or description to paste the scenario text or a link to the feature file; or use `--spec-id` / a custom field if your workflow supports it.
- **In Jira:** Put the Gherkin (or a link to the feature file) in the ticket description or acceptance criteria so Jira and the repo stay aligned.

---

## Tools (Optional)

- **Python:** `behave` (e.g. `features/` + step definitions in `steps/`).
- **Other:** Cucumber (Ruby/Java/JS), or any Gherkin parser. This guide is tool-agnostic; place and format matter most for agent generation.

---

*Last updated: March 2026*
