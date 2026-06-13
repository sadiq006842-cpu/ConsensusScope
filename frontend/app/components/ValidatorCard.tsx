"use client";

import { useState } from "react";
import { ChevronDown, Radio, ShieldAlert, Sparkles, Zap } from "lucide-react";
import type { SimulationValidator } from "@/lib/api";

interface ValidatorCardProps {
  validator: SimulationValidator;
}

function initials(name: string) {
  return name.split(" ").slice(0, 2).map((part) => part[0]).join("");
}

export default function ValidatorCard({ validator }: ValidatorCardProps) {
  const [expanded, setExpanded] = useState(false);
  const approved = validator.response === "APPROVE";
  const tags = [...validator.signals.red_flags.slice(0, 3), ...validator.signals.mitigations.slice(0, 3)];
  const intelligenceMetrics = [
    ["aggression", validator.aggression_level],
    ["decentralization", validator.decentralization_preference],
    ["memory pressure", validator.memory_pressure],
    ["trust", validator.trust_score],
    ["instability", validator.instability_contribution],
    ["influence", Math.round(validator.consensus_influence * 100)],
  ] as const;

  return (
    <article className={`relative overflow-hidden rounded-3xl border p-5 backdrop-blur transition hover:-translate-y-1 ${validator.disagrees ? "border-rose-300 bg-rose-50 shadow-[0_0_34px_rgba(244,63,94,0.16)]" : "border-violet-200 bg-white/80 shadow-[0_12px_28px_rgba(79,70,229,0.08)]"}`}>
      {validator.disagrees ? <span className="absolute right-5 top-5 h-3 w-3 rounded-full bg-rose-500 shadow-[0_0_20px_rgba(244,63,94,0.75)]"><span className="absolute inset-0 animate-ping rounded-full bg-rose-400" /></span> : null}
      <div className="flex items-start gap-4">
        <div className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl text-sm font-black ${approved ? "bg-emerald-50 text-emerald-700" : "bg-rose-50 text-rose-700"}`}>{initials(validator.validator)}</div>
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 className="font-bold text-slate-950">{validator.validator}</h3>
              <p className="mt-1 text-xs leading-5 text-slate-400">{validator.specialization}</p>
              <p className="mt-2 inline-flex items-center gap-1 rounded-full bg-violet-100 px-3 py-1 text-xs font-bold text-violet-700"><Radio size={12} /> {validator.philosophy || validator.personality}</p>
            </div>
            <span className={`rounded-full px-3 py-1 text-xs font-black ${approved ? "bg-emerald-50 text-emerald-700" : "bg-rose-50 text-rose-700"}`}>{validator.response}</span>
          </div>
          <div className="mt-4 rounded-2xl border border-slate-200 bg-white/70 p-3">
            <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.16em] text-slate-500"><Zap size={13} /> Intelligence profile</div>
            <p className="mt-2 text-sm text-slate-600">{validator.governance_bias || validator.personality}</p>
            <div className="mt-3 grid gap-3 sm:grid-cols-3">
              {intelligenceMetrics.map(([key, value]) => {
                const tone = key === "instability" && value > 45 ? "from-rose-400 to-orange-300" : "from-violet-500 to-indigo-400";
                return <div key={key}><div className="flex justify-between text-xs text-slate-500"><span>{key}</span><span>{value}%</span></div><div className="mt-1.5 h-2 rounded-full bg-slate-100"><div className={`h-2 rounded-full bg-gradient-to-r ${tone}`} style={{ width: `${Math.min(value, 100)}%` }} /></div></div>;
              })}
            </div>
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            {["confidence", "risk_score", "weight"].map((key) => {
              const value = key === "confidence" ? validator.confidence : key === "risk_score" ? validator.risk_score : Math.round(validator.weight * 100);
              return <div key={key}><div className="flex justify-between text-xs text-slate-400"><span>{key.replace("_", " ")}</span><span>{value}{key === "weight" ? "" : "%"}</span></div><div className="mt-1.5 h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-gradient-to-r from-violet-500 to-indigo-400" style={{ width: `${Math.min(value, 100)}%` }} /></div></div>;
            })}
          </div>
          <p className="mt-4 text-sm leading-6 text-slate-600">{validator.reasoning}</p>
          <div className="mt-4 flex flex-wrap gap-2">
            {validator.disagrees ? <span className="inline-flex items-center gap-1 rounded-full bg-rose-100 px-3 py-1 text-xs font-bold text-rose-700"><ShieldAlert size={13} /> Dissenting signal</span> : null}
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">{validator.recent_voting_trend || "new memory state"}</span>
            {tags.map((tag) => <span key={tag} className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">{tag}</span>)}
          </div>
          <button type="button" onClick={() => setExpanded((value) => !value)} className="mt-4 inline-flex items-center gap-2 text-sm font-bold text-violet-600">
            Reasoning trace <ChevronDown size={16} className={expanded ? "rotate-180 transition" : "transition"} />
          </button>
          {expanded ? (
            <div className="mt-4 rounded-2xl border border-violet-200 bg-violet-50/60 p-4">
              <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.18em] text-violet-600"><Sparkles size={14} /> Validator memory</p>
              <p className="mt-2 text-sm text-slate-400">{validator.memory_context.evaluations} reviews · {validator.memory_context.rejection_rate}% rejection rate · {validator.memory_context.high_risk_flags} high-risk flags</p>
              <ol className="mt-4 space-y-2 text-sm text-slate-600">
                {validator.reasoning_trace.map((trace) => <li key={trace} className="rounded-xl bg-white px-3 py-2">{trace}</li>)}
              </ol>
            </div>
          ) : null}
        </div>
      </div>
    </article>
  );
}
