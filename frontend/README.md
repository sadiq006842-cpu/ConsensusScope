# ConsensusScope Frontend

The frontend is a Next.js App Router application for the ConsensusScope Governance Intelligence Layer. It renders the landing experience, validator swarm command center, governance timeline, consensus heatmap, proposal history, and activity feed.

## Run

```powershell
npm install
npm.cmd run dev
```

Set `NEXT_PUBLIC_API_BASE_URL` when the FastAPI backend is not running at `http://127.0.0.1:8000`.

## Build

```powershell
npm.cmd run lint
npm.cmd run build
```

