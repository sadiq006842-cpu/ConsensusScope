import Link from "next/link";
import { ArrowRight, BadgeCheck, BrainCircuit, GitBranch, Megaphone, Rocket, ShieldCheck, Sparkles, Trophy } from "lucide-react";

const milestones = [
  {
    phase: "MVP",
    status: "Complete",
    title: "AI Validator Swarm Simulation",
    summary: "Four specialized validator personas review governance proposals with weighted consensus, confidence divergence, and visible disagreement.",
    proof: ["Sentinel, Civic, Atlas, Forge personas", "Weighted approve/reject scoring", "Proposal IDs and persisted traces"],
  },
  {
    phase: "V1",
    status: "Complete",
    title: "Governance Intelligence Layer",
    summary: "ConsensusScope adds validator memory, semantic risk amplification, prompt defense, attack scenarios, and governance activity logging.",
    proof: ["Validator memory pressure", "Risk engine modules", "Attack simulation library"],
  },
  {
    phase: "Submission",
    status: "Ready",
    title: "GenLayer Ecosystem Showcase",
    summary: "The app is packaged as an Optimistic Democracy observability surface for AI-native governance, intelligent validators, and trustless coordination.",
    proof: ["Docs route", "Architecture route", "Workflow trace route", "Health endpoint"],
  },
  {
    phase: "Growth",
    status: "Planned",
    title: "Live Intelligent Contract Handoff",
    summary: "Future milestones connect proposal traces to GenLayer intelligent contracts, validator reputation markets, and multi-round challenge simulation.",
    proof: ["GenLayer handoff", "Reputation analytics", "Cross-proposal anomaly detection"],
  },
];

const impactCards = [
  ["Ecosystem Value", "Makes Optimistic Democracy legible by visualizing validator reasoning, dissent, and adaptive consensus."],
  ["Builder Value", "Provides a reusable governance intelligence pattern for projects exploring AI-assisted decision systems."],
  ["Grant Use", "Supports deeper GenLayer integration, intelligent contract handoff, richer memory persistence, and public demo hardening."],
  ["Amplification", "Ready for demo clips, screenshots, architecture diagrams, and milestone updates through ecosystem channels."],
];

export default function MilestonesPage() {
  return (
    <main className="cs-shell min-h-screen px-6 py-10 text-slate-950 lg:px-10">
      <div className="mx-auto max-w-7xl">
        <header className="overflow-hidden rounded-[2rem] bg-black p-8 text-white shadow-[0_24px_80px_rgba(15,23,42,0.22)]">
          <Link href="/" className="text-sm font-bold text-violet-200">← ConsensusScope</Link>
          <div className="mt-10 grid gap-10 lg:grid-cols-[1.05fr_0.95fr] lg:items-end">
            <div>
              <p className="inline-flex items-center gap-2 rounded-full border border-violet-300/30 bg-white/10 px-4 py-2 text-xs font-bold uppercase tracking-[0.2em] text-violet-100">
                <Trophy size={14} /> Projects & Milestones
              </p>
              <h1 className="mt-6 max-w-4xl text-5xl font-black leading-[1.02] tracking-[-0.05em] md:text-7xl">
                From MVP to GenLayer ecosystem growth.
              </h1>
              <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">
                ConsensusScope is built as an AI-native governance intelligence layer that turns validator reasoning, disagreement, and risk into an observable Optimistic Democracy workflow.
              </p>
            </div>
            <div className="rounded-3xl border border-white/10 bg-white/10 p-6 backdrop-blur">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-violet-100">Shareable Summary</p>
              <p className="mt-3 text-2xl font-black">An AI governance operating system for intelligent validator coordination.</p>
              <div className="mt-5 flex flex-wrap gap-3">
                <Link href="/dashboard" className="rounded-full bg-violet-500 px-4 py-2 text-sm font-bold text-white">Launch Demo</Link>
                <Link href="/docs" className="rounded-full bg-white px-4 py-2 text-sm font-bold text-slate-950">Read Docs</Link>
              </div>
            </div>
          </div>
        </header>

        <section className="mt-8 grid gap-5 lg:grid-cols-4">
          {milestones.map((milestone, index) => {
            const icons = [Rocket, BrainCircuit, BadgeCheck, GitBranch];
            const Icon = icons[index];
            return (
              <article key={milestone.title} className="cs-panel cs-panel-hover rounded-3xl p-6">
                <div className="flex items-center justify-between gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-50 text-violet-600"><Icon size={20} /></div>
                  <span className={`rounded-full px-3 py-1 text-xs font-black ${milestone.status === "Planned" ? "bg-slate-100 text-slate-600" : "bg-emerald-50 text-emerald-700"}`}>{milestone.status}</span>
                </div>
                <p className="mt-5 text-xs font-bold uppercase tracking-[0.2em] text-violet-600">{milestone.phase}</p>
                <h2 className="mt-2 text-2xl font-black">{milestone.title}</h2>
                <p className="mt-3 text-sm leading-7 text-slate-500">{milestone.summary}</p>
                <ul className="mt-5 space-y-2 text-sm text-slate-600">
                  {milestone.proof.map((item) => <li key={item} className="flex gap-2"><Sparkles className="mt-0.5 shrink-0 text-violet-500" size={14} />{item}</li>)}
                </ul>
              </article>
            );
          })}
        </section>

        <section className="mt-8 grid gap-5 lg:grid-cols-[0.85fr_1.15fr]">
          <div className="cs-panel rounded-3xl p-7">
            <Megaphone className="text-violet-500" />
            <h2 className="mt-5 text-3xl font-black">Amplification Readiness</h2>
            <p className="mt-3 text-sm leading-7 text-slate-500">
              ConsensusScope is structured for GenLayer-style ecosystem updates: milestone proof, demo flow, technical docs, route-level architecture, and public roadmap are all visible.
            </p>
            <Link href="/workflow" className="mt-6 inline-flex items-center gap-2 rounded-full bg-black px-5 py-3 text-sm font-bold text-white">
              View Workflow <ArrowRight size={16} />
            </Link>
          </div>
          <div className="grid gap-5 md:grid-cols-2">
            {impactCards.map(([title, copy]) => (
              <article key={title} className="cs-panel cs-panel-hover rounded-3xl p-6">
                <ShieldCheck className="text-emerald-500" />
                <h3 className="mt-4 text-xl font-black">{title}</h3>
                <p className="mt-3 text-sm leading-7 text-slate-500">{copy}</p>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}
