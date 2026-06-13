import Link from "next/link";

const risks = ["Prompt injection", "Governance manipulation", "Economic coercion", "Consensus instability"];

export default function SecurityPage() {
  return <main className="cs-shell min-h-screen px-6 py-10 text-white lg:px-10"><div className="mx-auto max-w-6xl"><Link href="/" className="text-sm font-bold text-cyan-200">← Home</Link><h1 className="mt-8 text-5xl font-black tracking-[-0.04em]">Prompt Defense System</h1><p className="mt-4 max-w-3xl text-slate-300">A dynamic risk layer classifies adversarial input and governance anomalies before they can influence validator coordination.</p><div className="mt-10 grid gap-5 md:grid-cols-2">{risks.map((risk) => <article key={risk} className="cs-panel cs-panel-hover rounded-3xl p-6"><h2 className="text-2xl font-bold">{risk}</h2><p className="mt-3 text-sm leading-7 text-slate-300">Detected, scored, and attached to the proposal trace for downstream consensus review.</p></article>)}</div></div></main>;
}
