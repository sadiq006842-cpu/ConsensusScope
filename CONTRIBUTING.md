# Contributing

Thanks for improving ConsensusScope.

## Development Workflow

1. Keep frontend and backend changes modular.
2. Preserve existing API endpoints unless a migration is explicitly planned.
3. Add or update tests for backend intelligence changes.
4. Keep TypeScript strict and use shared API types from `frontend/lib/api.ts`.
5. Avoid frontend redesigns that remove governance intelligence functionality.

## Validation

```powershell
.\backend\venv\Scripts\python.exe -m pytest backend\tests -q
cd frontend
npm.cmd run lint
npm.cmd run build
```

## Code Style

- Backend: typed FastAPI routes, Pydantic response models, focused SQLAlchemy models.
- Frontend: reusable components, accessible labels where appropriate, responsive Tailwind layouts.
- Docs: update `docs/` when architecture, API contracts, or governance engine behavior changes.

