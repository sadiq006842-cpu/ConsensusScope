"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit, ShieldCheck, Sparkles, Network, Cpu, Radar } from "lucide-react";

const sectionCards = [
  { title: "Proposal Submission", text: "Governance intents enter a traceable protocol console with IDs, timestamps, and execution context." },
  { title: "Validator Review", text: "Specialized AI validators reason across security, civic legitimacy, economics, and technical feasibility." },
  { title: "Consensus Formation", text: "Optimistic Democracy weights confidence, disagreement, memory, and domain expertise into an auditable verdict." },
  { title: "Risk Detection", text: "Prompt injection, incentive drift, quorum manipulation, and consensus instability surface before execution." },
  { title: "Governance Execution", text: "Approved actions graduate into an execution trail with validator reasoning and challenge-period context." },
];

const validatorProfiles = [
  { name: "Sentinel", role: "Security", detail: "Confidence 91% · memory stable · approval cautious · disagreement 14%" },
  { name: "Civic", role: "Governance", detail: "Confidence 84% · memory adaptive · approval balanced · disagreement 22%" },
  { name: "Atlas", role: "Economic", detail: "Confidence 79% · memory treasury-aware · approval conservative · disagreement 31%" },
  { name: "Forge", role: "Technical", detail: "Confidence 88% · memory infra-heavy · approval pragmatic · disagreement 18%" },
];

const roadmap = [
  "Validator memory persistence",
  "Proposal history analytics",
  "Adaptive reputation evolution",
  "Attack simulation coverage",
  "Multi-chain governance expansion",
];

function GlowButton({ href, label, primary = false }: { href: string; label: string; primary?: boolean }) {
  return (
    <Link
      href={href}
      className={`cs-button inline-flex items-center gap-2 rounded-full px-5 py-3 text-sm font-semibold transition ${primary ? "bg-violet-500 text-white shadow-[0_0_28px_rgba(124,58,237,0.28)] hover:bg-violet-400" : "border border-slate-200 bg-white text-slate-950 hover:bg-slate-50"}`}
    >
      {label}
      <ArrowRight size={16} />
    </Link>
  );
}

export default function LandingPage() {
  return (
    <main className="cs-shell min-h-screen overflow-hidden text-slate-950">
      <section className="relative isolate px-6 pb-20 pt-5 lg:px-10">
        <div className="absolute inset-0 cs-grid opacity-20" />
        <div className="mx-auto max-w-7xl">
          <header className="relative z-10 flex flex-wrap items-center justify-between gap-4 border-b border-slate-200 bg-white/80 px-1 py-3 backdrop-blur">
            <div>
              <p className="text-xs uppercase tracking-[0.24em] text-violet-600">GenLayer Governance Intelligence</p>
              <h1 className="mt-1 text-xl font-black">ConsensusScope</h1>
            </div>
            <div className="flex flex-wrap gap-3">
              <GlowButton href="/dashboard" label="Open Dashboard" primary />
              <GlowButton href="/architecture" label="Architecture" />
              <GlowButton href="/docs" label="Documentation" />
              <GlowButton href="/milestones" label="Milestones" />
            </div>
          </header>

          <div className="mt-6 overflow-hidden rounded-[2rem] bg-black p-6 text-white shadow-[0_24px_80px_rgba(15,23,42,0.18)] lg:p-10">
          <div className="grid gap-14 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div>
              <motion.p initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} className="inline-flex items-center gap-2 rounded-full border border-violet-300/40 bg-white/10 px-4 py-2 text-xs font-bold uppercase tracking-[0.18em] text-violet-100">
                <Sparkles size={14} /> Optimistic Democracy Engine
              </motion.p>
              <motion.h2 initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.08 }} className="mt-6 max-w-4xl text-5xl font-black leading-[1.02] tracking-[-0.05em] md:text-7xl">
                GenLayer Validator Intelligence.
              </motion.h2>
              <motion.p initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.16 }} className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
                ConsensusScope turns competing AI validator priorities into a live Optimistic Democracy simulation with conflict, memory, risk asymmetry, and weighted consensus.
              </motion.p>
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.24 }} className="mt-8 flex flex-wrap gap-3">
                <GlowButton href="/dashboard" label="Launch Demo" primary />
                <GlowButton href="/workflow" label="Explore Workflow" />
              </motion.div>

              <div className="mt-10 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
                {[
                  ["Validator Swarm", "4 personas"],
                  ["Weighted Consensus", "Adaptive score"],
                  ["Risk Intelligence", "Attack aware"],
                  ["Memory Layer", "Persistent context"],
                ].map(([label, value]) => (
                  <div key={label} className="rounded-3xl border border-white/10 bg-white/10 p-4 backdrop-blur">
                    <p className="text-xs uppercase tracking-[0.16em] text-slate-400">{label}</p>
                    <p className="mt-3 text-2xl font-bold text-white">{value}</p>
                  </div>
                ))}
              </div>
            </div>

            <motion.div initial={{ opacity: 0, scale: 0.96 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.12 }} className="relative overflow-hidden rounded-[2rem] border border-white/15 bg-white/10 p-6 backdrop-blur">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(124,58,237,0.34),transparent_42%)]" />
              <div className="relative">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs uppercase tracking-[0.2em] text-violet-100">Live Demo Preview</p>
                    <h3 className="mt-1 text-xl font-bold">Consensus Snapshot</h3>
                  </div>
                  <span className="rounded-full bg-emerald-400/15 px-3 py-1 text-xs font-bold text-emerald-200">LOW RISK</span>
                </div>
                <div className="mt-6 grid gap-4 sm:grid-cols-2">
                  {validatorProfiles.map((profile, index) => (
                    <motion.div key={profile.name} animate={{ y: [0, -6, 0] }} transition={{ duration: 2.5 + index * 0.2, repeat: Infinity }} className="rounded-3xl border border-white/10 bg-white/10 p-4">
                      <p className="text-xs uppercase tracking-[0.18em] text-slate-400">{profile.role}</p>
                      <h4 className="mt-2 text-lg font-semibold">{profile.name}</h4>
                      <p className="mt-2 text-sm leading-6 text-slate-300">{profile.detail}</p>
                    </motion.div>
                  ))}
                </div>
                <div className="mt-5 rounded-3xl border border-white/10 bg-slate-950/70 p-5">
                  <div className="flex items-center justify-between text-sm"><span className="text-slate-400">Consensus agreement</span><span className="font-bold text-white">78.7%</span></div>
                  <div className="mt-3 h-2 rounded-full bg-white/10"><div className="h-2 w-[79%] rounded-full bg-gradient-to-r from-cyan-300 via-violet-400 to-emerald-300" /></div>
                  <p className="mt-4 text-sm text-slate-400">Validators disagree when risk domains diverge. The system preserves nuance instead of flattening results into a binary vote.</p>
                </div>
              </div>
            </motion.div>
          </div>
          </div>
        </div>
      </section>

      <section id="architecture" className="px-6 py-20 lg:px-10">
        <div className="mx-auto max-w-7xl">
          <p className="text-xs font-bold uppercase tracking-[0.22em] text-violet-600">Governance workflow</p>
          <h3 className="mt-3 max-w-3xl text-3xl font-black md:text-5xl">From proposal intent to trustless execution.</h3>
          <div className="mt-10 grid gap-5 md:grid-cols-2 xl:grid-cols-5">
          {sectionCards.map((card, index) => (
            <article key={card.title} className="cs-panel cs-panel-hover relative rounded-3xl p-6">
              <span className="absolute -right-3 top-1/2 hidden text-violet-300 xl:block">{index < sectionCards.length - 1 ? "↓" : ""}</span>
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-50 text-violet-600"><Cpu size={20} /></div>
              <h3 className="mt-5 text-xl font-bold">{card.title}</h3>
              <p className="mt-3 text-sm leading-6 text-slate-500">{card.text}</p>
            </article>
          ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-16 lg:px-10">
        <div className="mx-auto grid max-w-7xl gap-6 rounded-[2rem] bg-black p-8 text-white lg:grid-cols-[0.9fr_1.1fr] lg:p-10">
          <div>
            <p className="text-xs font-bold uppercase tracking-[0.22em] text-violet-200">Projects & Milestones</p>
            <h3 className="mt-3 text-4xl font-black tracking-[-0.04em] md:text-5xl">Built to show progress from MVP to ecosystem growth.</h3>
            <p className="mt-4 text-sm leading-7 text-slate-300">ConsensusScope packages working product proof, governance intelligence milestones, and future GenLayer integration goals into a submission-ready project story.</p>
            <Link href="/milestones" className="mt-6 inline-flex items-center gap-2 rounded-full bg-violet-500 px-5 py-3 text-sm font-bold text-white">
              View Milestones <ArrowRight size={16} />
            </Link>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {[
              ["MVP", "Validator swarm, weighted consensus, proposal traces"],
              ["V1", "Memory, attack scenarios, disagreement heatmap"],
              ["Submission", "Docs, workflow, architecture, health endpoint"],
              ["Growth", "Intelligent contract handoff and reputation analytics"],
            ].map(([phase, detail]) => (
              <div key={phase} className="rounded-3xl border border-white/10 bg-white/10 p-5 backdrop-blur">
                <p className="text-xs font-bold uppercase tracking-[0.2em] text-violet-100">{phase}</p>
                <p className="mt-3 text-sm leading-6 text-slate-300">{detail}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="px-6 py-20 lg:px-10">
        <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[0.95fr_1.05fr]">
          <div className="cs-panel rounded-3xl p-8">
            <p className="text-xs uppercase tracking-[0.2em] text-violet-600">Architecture</p>
            <h3 className="mt-3 text-3xl font-black">Governance Intelligence Layer</h3>
            <p className="mt-4 text-sm leading-7 text-slate-500">
              FastAPI persists proposal history, validator decisions, governance events, and analytics tables. Next.js renders a cinematic control center with live risk, swarm, and timeline visualizations.
            </p>
            <div className="mt-6 space-y-3 text-sm text-slate-600">
              <p>• Backend: FastAPI + SQLite + OpenAI + weighted consensus</p>
              <p>• Frontend: Next.js App Router + TypeScript + Tailwind + Framer Motion</p>
              <p>• Intelligence: validator memory, risk analysis, attack simulation, disagreement tracking</p>
            </div>
          </div>
          <div className="grid gap-5 sm:grid-cols-2">
            <div className="cs-panel rounded-3xl p-6">
              <Network className="text-violet-500" />
              <h4 className="mt-4 text-lg font-semibold">Consensus Visualization</h4>
              <p className="mt-2 text-sm leading-6 text-slate-500">Animated validator swarm nodes, heatmaps, and timeline sequencing make governance reasoning visible.</p>
            </div>
            <div className="cs-panel rounded-3xl p-6">
              <ShieldCheck className="text-emerald-500" />
              <h4 className="mt-4 text-lg font-semibold">Risk Intelligence</h4>
              <p className="mt-2 text-sm leading-6 text-slate-500">Prompt injection, economic manipulation, and governance anomaly detection run before execution.</p>
            </div>
            <div className="cs-panel rounded-3xl p-6">
              <BrainCircuit className="text-violet-500" />
              <h4 className="mt-4 text-lg font-semibold">Validator Personas</h4>
              <p className="mt-2 text-sm leading-6 text-slate-500">Security, governance, economic, and technical validators maintain unique personalities and memory.</p>
            </div>
            <div className="cs-panel rounded-3xl p-6">
              <Radar className="text-fuchsia-500" />
              <h4 className="mt-4 text-lg font-semibold">Future Roadmap</h4>
              <ul className="mt-2 space-y-2 text-sm text-slate-500">
                {roadmap.map((item) => <li key={item}>• {item}</li>)}
              </ul>
            </div>
          </div>
        </div>
      </section>

      <footer className="px-6 py-12 lg:px-10">
        <div className="mx-auto flex max-w-7xl flex-col gap-4 rounded-3xl border border-slate-200 bg-white/80 p-6 text-sm text-slate-500 md:flex-row md:items-center md:justify-between">
          <p>ConsensusScope · GenLayer Governance Intelligence · AI Validator Swarm</p>
          <div className="flex gap-4">
            <Link href="/dashboard" className="text-violet-600">Dashboard</Link>
            <a href="https://www.genlayer.com/" target="_blank" rel="noreferrer" className="text-violet-600">GenLayer</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
