# API

All response payloads are schema-validated with Pydantic and mirrored in the frontend TypeScript types.

## Routes

- `GET /` — service health and identity.
- `GET /validators` — persisted validator snapshot.
- `POST /validators` — add validator record.
- `DELETE /validators/cleanup` — legacy cleanup utility.
- `POST /analyze-prompt` — prompt injection and dynamic risk analysis.
- `POST /simulate-consensus` — full AI validator swarm simulation.
- `POST /submit-to-genlayer` — deployment handoff payload.
- `POST /test-gpt` — single-validator reasoning probe.
- `GET /governance/history` — proposal history.
- `GET /governance/events` — governance event log.
- `GET /governance/metrics` — governance analytics.

## Response Guarantees

- Consensus results always include weighted and non-weighted scores.
- Every validator result includes reasoning, trace, signals, memory, confidence, and disagreement state.
- Risk analysis always includes category-level scores and prompt-injection signals.
- API responses are stable enough for dashboard rendering and contract testing.

