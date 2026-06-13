# Architecture

ConsensusScope is layered as a governance intelligence platform rather than a single simulation screen.

```text
User Proposal
  -> PromptRequest schema
  -> Dynamic Risk Analysis
  -> Validator Persona Evaluation
  -> Weighted Consensus Calculation
  -> Optimistic Democracy Rounds
  -> Persistence + Analytics
  -> Dashboard Visualizations
```

## Backend

- `backend/main.py` hosts FastAPI routes, Pydantic response contracts, SQLAlchemy models, logging, persistence helpers, and the governance engine.
- `backend/fallback_responses.py` provides deterministic offline intelligence when OpenAI is unavailable.
- `backend/tests/` validates consensus math, schema contracts, prompt injection detection, and fallback behavior.

## Frontend

- `frontend/app/landing/page.tsx` renders the premium product landing page.
- `frontend/app/dashboard/page.tsx` renders the governance command center.
- `frontend/app/components/` contains reusable intelligence panels, cards, logs, sidebar, and topbar.
- `frontend/lib/api.ts` centralizes strict TypeScript API contracts and retry handling.

## Persistence Diagram

```text
proposals
  ├─ validator_decisions
  ├─ governance_events
  └─ proposal_analytics

validator_memory
  └─ evolving behavioral context per validator
```

