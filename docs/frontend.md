# Frontend

The frontend is built with Next.js App Router, TypeScript, TailwindCSS, Framer Motion, and reusable command-center components.

## Routes

- `/` and `/landing` — premium ConsensusScope product landing page.
- `/dashboard` — governance intelligence command center.

## Component System

- `IntelligenceVisuals.tsx` — swarm visualization, heatmap, timeline, metrics, history, activity feed, skeletons, and empty states.
- `ValidatorCard.tsx` — validator decision, confidence, specialization, concerns, mitigations, memory, and reasoning trace.
- `StatsCard.tsx` — metric summaries.
- `Sidebar.tsx` and `Topbar.tsx` — command center navigation and wallet connection.
- `LogPanel.tsx` — API and governance activity visibility.

## API Handling

`frontend/lib/api.ts` defines TypeScript contracts for backend responses and centralizes retry-aware API calls.

## Visual Direction

The UI uses dark glassmorphism, neon governance accents, animated validator nodes, smooth transitions, and responsive layouts to create an AI-native governance control center feel.

