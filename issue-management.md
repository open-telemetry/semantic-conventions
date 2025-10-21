# Issue and PR triage management

This document outlines the triage process for the Semantic Conventions project,
including role definitions and the labels used throughout the workflow.

## Roles

- **Author**:
  The person who has opened the issue or pull request.

- **Collaborator**:
  The person or people responsible for performing the work related to the issue
  or pull request. They may or may not be the same as the Author. Collaborators
  interact with the Reviewer to receive feedback on the changes.

- **Reviewer**:
  The person whose approval is required to merge the pull request. Reviewers may
  include general Semantic Conventions approvers, maintainers, or code owners.

- **Triager**:
  The person responsible for applying the triage process and labels as outlined
  below. Triagers work closely with the Author to analyze the issue or pull
  request and provide relevant details, information, or guidance to aid in its
  resolution.

## Issue triage

Triagers apply the workflow and labels defined below to indicate the current
stage of an issue in the triage process. Labels are grouped into three main
categories: `deciding`, `accepted`, and `rejected`. Each category contains
specific sub-labels that provide additional context

```mermaid
graph TD
    START([New Issue]) --> AUTO_ASSIGN["Auto-assign labels: **area:*** and **triage:needs-triage**"]
    AUTO_ASSIGN--> TRIAGE["Triagers engage to decide<br> triage result"]
    TRIAGE --> TRIAGE_CONCLUSION["Reach conclusion:
            remove label
            **triage:needs-triage** and
            assign label **triage:***"]

    TRIAGE_CONCLUSION --> NEEDS_INFO{Needs clarification?}
    NEEDS_INFO -->|Yes| L_NEEDS_INFO([Label: **triage:deciding:needs-info**])
    L_NEEDS_INFO --> UNRESPONSIVE{Unresponsive for 3 months?}
    UNRESPONSIVE -->|Yes| L_INSUFFICIENT_INFO([Close with label: **triage:rejected:insufficient-info**])
    UNRESPONSIVE -->|No| FEEDBACK_PROVIDED["Community provides feedback (use cases, design proposals, prototypes)"]
    FEEDBACK_PROVIDED --> SIG_EXISTS{Does a SIG/project exist?}
    SIG_EXISTS -->|Yes| L_READY_SIG
    SIG_EXISTS -->|No| L_NEEDS_SIG([Label: **triage:accepted:needs-sig**])
    L_NEEDS_SIG --> SIG_FORMED[SIG/Project formed]
    SIG_FORMED --> L_READY_SIG
    L_NEEDS_SIG --> SIG_REJECTED[SIG rejected issue]
    SIG_REJECTED --> REJECTED([Label: triage:rejected:declined])
    L_READY_SIG([Label: **triage:accepted:ready-with-sig**])

    NEEDS_INFO -->|No| L_CHECK_SCOPE{What's the scope of the issue?}
    L_CHECK_SCOPE -->|Small or Trivial| L_READY([Label: **triage:accepted:ready**])
    L_CHECK_SCOPE -->|Other| SIG_EXISTS{Does a SIG/project exist?}

    %% Define Classes
    classDef styleStart fill:#c6dcff,stroke:#498bf5,stroke-width:2px,color:#000,font-size:1.2em;
    classDef styleRejected fill:#FFCCCC,stroke:#FF0000,stroke-width:2px,color:#000;
    classDef styleAccepted fill:#adf0c7,stroke:#00AA00,stroke-width:2px,color:#000;
    classDef styleLabel fill:#fff6b6,stroke:#bfad2c,stroke-width:2px,color:#000;

    %% Assign Classes to Nodes
    class START styleStart;
    class REJECTED,L_INSUFFICIENT_INFO styleRejected;
    class L_READY,L_READY_SIG styleAccepted;
    class L_NEEDS_INFO,L_NEEDS_SIG styleLabel;
```

### Labels

#### `triage:deciding:*`

These labels are applied to issues when it is not yet clear if the project will
address them.

- `triage:deciding:needs-info`: Indicates that the issue lacks sufficient
  information for the project to accept it. The issue remains open to allow the
  Author to add the requested details.

#### `triage:rejected:*`

Rejected issues describe problems that cannot or will not be addressed by the
project in their current form.

- `triage:rejected:declined`
- `triage:rejected:duplicate`
- `triage:rejected:insufficient-info`
- `triage:rejected:out-of-scope`

#### `triage:accepted:*`

These labels are applied to issues that describe a problem within the project's
scope. Acceptance of an issue does not guarantee that the suggested solution
will be implemented

- `triage:accepted:ready` - The issue is ready to be implemented. It is either
  small in scope or uncontroversial enough to proceed without requiring a SIG.

- `triage:accepted:ready-with-sig` - The issue is ready to be implemented
  and has an active SIG for the relevant area.

- `triage:accepted:needs-sig` - The issue is ready to be implemented, but a
  new SIG must first be formed.
  Pull requests for such issues will be automatically closed.

## Pull request triage

### General rules

1. **Issue link requirement**
   - All pull requests **must be linked to an issue** that has the
     `triage:accepted:ready*` or `triage:accepted:ready-with-sig` label.

2. **Semantic convention areas without active SIG/project**
   - PRs modifying semantic conventions **without an active SIG/project** (see
     [Semantic Convention Areas](./AREAS.md)) will be **automatically closed**
     with the label `triage:rejected:declined`.
   - **Override Process**: Maintainers/approvers can override this automation by:
     - Adding the label `triage:accepted:ready` to the PR.
     - Re-opening the PR.

3. **Rejection of Non-Compliant PRs**
   - Any PR that does not meet the above requirements will be **rejected** with
     the label `triage:rejected:declined`.

### Exceptions

The following types of PRs are exempt from the above general rules:

1. **PRs originating from SIGs**
   - PRs submitted directly by Special Interest Groups (SIGs) members.

2. **Automated PRs**
   - PRs generated by automation tools (e.g., Renovate).

3. **Trivial changes**
   - PRs containing minor changes, such as:
     - Typos.
     - Styling-only updates.
     - Tooling improvements.

```mermaid
flowchart TD
    START(["New pull request"]) -->IS_TRIVIAL{"Trivial changes?"}
    START -->HAS_ACTIVE_SIG{"Has active SIG?"}
    HAS_ACTIVE_SIG --> |No| L_END_DECLINED
    IS_TRIVIAL -->|No| HAS_LINKED_ISSUE{"Linked to triaged issue?"}
    HAS_LINKED_ISSUE -->|No| L_END_DECLINED(["PR is closed unmerged with label: **triage:rejected:declined**"])
    HAS_LINKED_ISSUE -->|Yes| L_END_ACCEPTED
    L_END_ACCEPTED --> PR_REVIEW["PR reviewed by maintainers/code owners"]
    PR_REVIEW --> L_END_DECLINED
    PR_REVIEW --> PR_MERGED(["PR merged and issue is closed as done"])
    L_END_ACCEPTED(["Add label **triage:accepted:ready**"])
    IS_TRIVIAL -->|Yes| L_END_ACCEPTED

    %% Define Classes
    classDef styleStart fill:#c6dcff,stroke:#498bf5,stroke-width:2px,color:#000,font-size:1.1em;
    classDef styleRejected fill:#FFCCCC,stroke:#FF0000,stroke-width:2px,color:#000;
    classDef styleAccepted fill:#adf0c7,stroke:#00AA00,stroke-width:2px,color:#000;
    classDef styleLabel fill:#fff6b6,stroke:#bfad2c,stroke-width:2px,color:#000;

    %% Assign Classes to Nodes
    class START styleStart;
    class L_END_DECLINED styleRejected;
    class L_END_ACCEPTED,PR_MERGED styleAccepted;
```
