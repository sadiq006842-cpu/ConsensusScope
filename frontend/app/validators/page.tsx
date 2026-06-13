import Link from "next/link";

const validators = [["Sentinel", "Security", "Exploit vectors, injection risk, protocol integrity"], ["Civic", "Governance", "Fairness, legitimacy, quorum resilience"], ["Atlas", "Economic", "Incentives, treasury health, sustainability"], ["Forge", "Technical", "Scalability, infrastructure, reliability"]];

export default function ValidatorsPage() {
  return <main className="cs-shell min-h-screen px-6 py-10 text-white lg:px-10"><div className="mx-auto max-w-6xl"><Link href="/" className="text-sm font-bold text-cyan-200">← Home</Link><h1 className="mt-8 text-5xl font-black tracking-[-0.04em]">AI Validator Swarm</h1><p className="mt-4 max-w-3xl text-slate-300">Validator personas coordinate specialized reasoning while preserving disagreement as a first-class governance signal.</p><div className="mt-10 grid gap-5 md:grid-cols-2">{validators.map(([name, role, text]) => <article key={name} className="cs-panel cs-panel-hover rounded-3xl p-6"><p className="text-xs uppercase tracking-[0.2em] text-cyan-200">{role}</p><h2 className="mt-3 text-3xl font-black">{name}</h2><p className="mt-3 text-sm leading-7 text-slate-300">{text}</p></article>)}</div></div></main>;
}
