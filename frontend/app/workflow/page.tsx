import Link from "next/link";
import { ArrowRight, Brain, GitBranch, Radar, ShieldAlert, Sparkles, Zap } from "lucide-react";

const steps = [
  ["Proposal Submitted", "A governance intent enters the AI consensus layer with semantic category and proposal fingerprint."],
  ["Validator Activation", "Sentinel, Civic, Atlas, and Forge activate with different trust thresholds and domain priorities."],
  ["Risk Signals Triggered", "Security, governance, economic, coordination, and manipulation vectors amplify dynamically."],
  ["Persona Analysis", "Each validator applies memory, philosophy, aggression, and specialization to form a position."],
  ["Disagreement Formation", "Confidence divergence, red flags, and ideology create consensus fracture when needed."],
  ["Weighted Consensus", "Influence paths combine trust, expertise relevance, confidence, and dissent pressure."],
  ["Governance Resolution", "The system emits verdict, challenge window, anomaly score, and execution trace."],
];

const signals = ["consensus fracture", "high dissent", "unstable majority", "coordinated alignment"];

export default function WorkflowPage() {
  return (
    <main className="cs-shell min-h-screen px-6 py-10 text-slate-950 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="rounded-[2rem] bg-black p-8 text-white shadow-[0_24px_80px_rgba(15,23,42,0.2)]">
          <Link href="/" className="text-sm font-bold text-violet-200">← ConsensusScope</Link>
          <p className="mt-8 text-xs font-bold uppercase tracking-[0.24em] text-violet-200">Execution Workflow</p>
          <h1 className="mt-3 max-w-4xl text-5xl font-black tracking-[-0.05em] md:text-7xl">Optimistic Democracy trace engine.</h1>
          <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">A visual governance pipeline for non-deterministic validator coordination, conflict formation, and trustless AI-assisted consensus.</p>
        </header>

        <section className="mt-8 grid gap-4 lg:grid-cols-7">
          {steps.map(([title, detail], index) => {
            const icons = [Sparkles, Brain, Radar, ShieldAlert, GitBranch, Zap, ArrowRight];
            const Icon = icons[index];
            return (
              <article key={title} className="cs-panel cs-panel-hover relative rounded-3xl p-5">
                <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-violet-50 text-violet-600"><Icon size={18} /></div>
                <p className="mt-5 text-xs font-bold uppercase tracking-[0.18em] text-slate-400">Step {index + 1}</p>
                <h2 className="mt-2 text-lg font-black">{title}</h2>
                <p className="mt-3 text-sm leading-6 text-slate-500">{detail}</p>
              </article>
            );
          })}
        </section>

        <section className="mt-8 grid gap-4 md:grid-cols-4">
          {signals.map((signal) => (
            <div key={signal} className="rounded-3xl border border-violet-200 bg-white/80 p-5">
              <p className="text-xs font-bold uppercase tracking-[0.18em] text-violet-600">Signal</p>
              <p className="mt-2 text-xl font-black capitalize">{signal}</p>
            </div>
          ))}
        </section>
      </div>
    </main>
  );
}
