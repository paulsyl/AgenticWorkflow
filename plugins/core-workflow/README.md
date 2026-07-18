# Core Workflow Plugin (v2.0)

Composable agent skills for the Grounded Software Development Lifecycle (SDLC). Each skill is independently invocable — use the right tool for the job. The orchestrator chains them optionally for the full ceremony.

## Quick Reference

| Skill | What it does | Invoke |
|---|---|---|
| **specifier-grill** | Round-based grilling to align understanding | `@specifier-grill` |
| **specifier-prd** | Generate immutable PRD from aligned understanding | `@specifier-prd` |
| **architect** | Translate PRD into vertical-sliced technical phases | `@architect` |
| **review-council** | Validate architecture (4 core + 3 optional reviewers) | `@review-council` |
| **executor** | Build code phase-by-phase with escape hatches | `@executor` |
| **orchestrator** | Full pipeline (optional — chains all stages) | `@orchestrator` |
| **prototype** | Throwaway exploration — no ceremony | `@prototype` |
| **setup-core-workflow** | Per-repo configuration | `@setup-core-workflow` |

## First-Time Setup

Run `/setup-core-workflow` once per repo. It creates the `AgentWorkflow/` directory structure, a `CONTEXT.md` domain glossary template, and project-specific configuration.

## The SDLC Pipeline (Optional)

When you want the full ceremony, invoke `@orchestrator`. It chains all stages automatically:

```mermaid
flowchart TD
    Start([User Request]) --> Grill[fa:fa-search @specifier-grill]
    Grill <--> |Interrogation Loop| Human[Human Clarification]
    Grill --> PRD[@specifier-prd]
    PRD --> |Output: PRD.md| Architect[fa:fa-sitemap @architect]
    
    Architect --> |Output: Phase-*.md| Review[fa:fa-gavel @review-council]
    Review <--> |Validation Loop| Architect
    
    Review --> |All 4 Core PASS| Executor[fa:fa-cogs @executor]
    
    subgraph Execution Loop
        Executor --> |Reads Phase-*.md| Code[Writes Code]
        Code --> Validate[Run validation]
        Validate -- Pass --> Status[Mark Complete]
        Status --> NextPhase{More Phases?}
        NextPhase -- Yes --> Executor
        
        Validate -- Fail --> Fix[Attempt Fix]
        Fix --> Validate2[Re-validate]
        Validate2 -- Pass --> Status
        Validate2 -- Fail --> Limit{3rd Failure?}
        Limit -- No --> Fix
        Limit -- Yes --> Rollback[fa:fa-undo Rollback & Exception]
        Rollback --> Architect
    end
    
    NextPhase -- No --> Finish([All Phases Complete])
```

## Composable Usage

For most tasks, invoke individual skills directly:

- **Bug fix:** `@executor` (skip straight to building)
- **Exploration:** `@prototype` (throwaway code, no PRD)
- **New feature:** `@specifier-grill` → `@specifier-prd` → `@architect` → `@review-council` → `@executor`
- **Full ceremony:** `@orchestrator`

## Architecture Decision Records

See `adr/` for documented decisions:
- [0001: Composable Over Monolithic](adr/0001-composable-over-monolithic.md)
- [0002: Four Core Reviewers](adr/0002-four-core-reviewers.md)
- [0003: Vertical Slicing Default](adr/0003-vertical-slicing-default.md)

## Artifact Directory Structure

Created by `/setup-core-workflow`:

```text
AgentWorkflow/
├── 00_scope/                  
│   ├── Project-scope.md
│   └── CONTEXT.md             # Domain glossary
├── 01_requirements/           
│   └── <phase_name>/PRD.md    
├── 02_architecture/           
│   ├── System-Architecture.md 
│   └── iterations/
│       └── <iteration_name>/
│           ├── Phase-1.md     # Vertical slices
│           └── Phase-2.md
├── 03_reviews/                
│   └── review_log.md          
└── 04_execution/              
    └── PROGRESS.md            
```

## QA Testing

Black-box QA testing is available via the separate `qa-workflow` plugin. It chains after execution as an optional quality gate.
