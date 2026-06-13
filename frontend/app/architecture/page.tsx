import Link from "next/link";

const layers = ["Next.js governance console", "FastAPI intelligence API", "Validator memory and proposal history", "Risk engine and prompt defense", "Optimistic Democracy execution trail"];

export default function ArchitecturePage() {
  return <main className="cs-shell min-h-screen px-6 py-10 text-white lg:px-10"><div className="mx-auto max-w-6xl"><Link href="/" className="text-sm font-bold text-cyan-200">← Home</Link><h1 className="mt-8 text-5xl font-black tracking-[-0.04em]">Governance Intelligence Architecture</h1><p className="mt-4 max-w-3xl text-slate-300">ConsensusScope aligns UI, API, validator reasoning, and protocol logs into a GenLayer-style operating system for trustless decision systems.</p><div className="mt-10 space-y-4">{layers.map((layer, index) => <div key={layer} className="cs-panel cs-panel-hover rounded-3xl p-6"><p className="text-xs uppercase tracking-[0.2em] text-cyan-200">Layer {index + 1}</p><h2 className="mt-2 text-2xl font-bold">{layer}</h2></div>)}</div></div></main>;
}
