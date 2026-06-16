# ConsensusScope

ConsensusScope is a production-grade AI Governance Intelligence Platform for the GenLayer ecosystem. It combines a Next.js command center with a FastAPI governance engine to simulate AI validator swarms, weighted consensus, disagreement analysis, prompt-injection defense, and persistent governance intelligence.

## Core Capabilities

- AI Validator Swarm with security, governance, economic, and technical personas.
- Optimistic Democracy Engine with weighted consensus and challenge-period metadata.
- Governance Risk Engine for prompt injection, economic manipulation, capture risk, and anomaly detection.
- Persistent proposal history, validator decisions, event logs, memory, and analytics in SQLite.
- Governance attack scenario library for treasury drain, validator cartel, quorum manipulation, inflation attacks, malicious emergency upgrades, and prompt injection.
- Validator intelligence cards exposing philosophy, governance bias, aggression level, memory pressure, trust score, consensus influence, and instability contribution.
- Cinematic governance command center built with Next.js, TypeScript, TailwindCSS, Framer Motion, and Recharts-ready data models.

## Architecture

```text
Next.js App Router UI
  -> typed API client with retry handling
  -> FastAPI response schemas
  -> Governance Engine
  -> Semantic risk amplification + proposal analysis cache
  -> SQLite persistence
  -> OpenAI SDK with deterministic fallback intelligence
```

## Routes

- `/` landing page
- `/dashboard` governance command center
- `/docs` product and API documentation
- `/architecture` architecture overview
- `/workflow` Optimistic Democracy execution pipeline
- `/milestones` project milestones, grant framing, and ecosystem impact
- `/validators` validator persona overview
- `/security` prompt defense overview

## API Overview

- `GET /health` service readiness, database status, validator count, OpenAI mode.
- `POST /simulate-consensus` runs validator swarm analysis and persists proposal trace.
- `POST /analyze-prompt` runs prompt injection and semantic risk detection.
- `GET /governance/history` returns persisted proposal history.
- `GET /governance/events` returns governance event logs.
- `GET /governance/metrics` returns aggregate governance intelligence metrics.

## Local Setup

### Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload
```

### Frontend

```powershell
cd frontend
npm install
npm.cmd run dev
```

Open `https://consensus-scope.vercel.app`.

## Environment Variables

- `OPENAI_API_KEY`: optional; when absent, deterministic validator fallback intelligence is used.
- `CONSENSUSSCOPE_USE_LLM_VALIDATORS`: set `true` to allow OpenAI-assisted validator responses; defaults to deterministic heuristics for demo stability.
- `DATABASE_URL`: optional SQLAlchemy URL, defaults to `sqlite:///./consensus.db`.
- `GENLAYER_CONTRACT_ADDRESS`: optional deployed governance contract address.
- `NEXT_PUBLIC_API_BASE_URL`: optional frontend API base, defaults to `http://127.0.0.1:8000`.

### Landing Page
![Landing](https://consensus-scope.vercel.app)

### Live Deployment
- 🌐 Frontend: https://consensus-scope.vercel.app
- ⚙️ Backend API: https://consensusscope-backend.onrender.com
- 📡 API Docs: https://consensusscope-backend.onrender.com/docs
- 🔗 Contract: https://explorer-bradbury.genlayer.com/tx/0x375eabbfb73944f1f9440e360c4f83d75d418f4a82b414892b06962d5846b498

## Projects & Milestones

ConsensusScope is structured to show clear progress from MVP to ecosystem growth:

| Phase | Status | Milestone | Proof |
| --- | --- | --- | --- |
| MVP | Complete | AI validator swarm simulation | Four validator personas, weighted consensus, proposal IDs, persisted traces |
| V1 | Complete | Governance intelligence layer | Memory pressure, semantic risk amplification, prompt defense, attack scenario library |
| Submission | Ready | GenLayer ecosystem showcase | `/docs`, `/architecture`, `/workflow`, `/milestones`, `/health`, README, `.env.example` |
| Growth | Planned | Live intelligent contract handoff | GenLayer execution handoff, reputation analytics, multi-round challenge simulation |

### Ecosystem Impact

- Makes Optimistic Democracy easier to understand through visual validator reasoning and dissent.
- Demonstrates how AI validators can coordinate without collapsing into generic agreement.
- Provides a reusable governance intelligence pattern for builders experimenting with intelligent contracts.
- Creates a shareable project story for ecosystem amplification: working demo, architecture, workflow, milestones, and roadmap.

### Grant Use

Future grant support would accelerate:

- Live GenLayer intelligent contract integration.
- Persistent vector/embedding-backed proposal similarity.
- Validator reputation and reliability scoring.
- Challenge-period simulation and governance resolution analytics.
- Public deployment polish, screenshots, demo video, and ecosystem documentation.

## Roadmap

- Live intelligent contract handoff.
- Persistent vector/embedding-backed proposal similarity.
- Multi-round challenge simulation.
- Validator reputation markets.
- Cross-proposal coordination anomaly detection.

## Validation

```powershell
.\backend\venv\Scripts\python.exe -m pytest backend\tests -q
cd frontend
npm.cmd run lint
npm.cmd run build
```

## Documentation

- `docs/architecture.md`
- `docs/api.md`
- `docs/governance-engine.md`
- `docs/validators.md`
- `docs/frontend.md`
- `CONTRIBUTING.md`
