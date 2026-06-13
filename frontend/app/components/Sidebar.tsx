import { Activity, Brain, Settings, ShieldAlert, ShieldCheck, TerminalSquare } from "lucide-react";
import Link from "next/link";

export type ActivePage = "Overview" | "Validators" | "Consensus" | "Security" | "Activity" | "Settings";

interface SidebarProps {
  activePage: ActivePage;
  setActivePage: (page: ActivePage) => void;
}

const navItems: Array<{ label: ActivePage; icon: typeof Activity }> = [
  { label: "Overview", icon: Activity },
  { label: "Validators", icon: ShieldCheck },
  { label: "Consensus", icon: Brain },
  { label: "Security", icon: ShieldAlert },
  { label: "Activity", icon: TerminalSquare },
  { label: "Settings", icon: Settings },
];

function ConsensusScopeLogo() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <polygon points="16,2 30,10 30,22 16,30 2,22 2,10" fill="#1B2B6B" stroke="#1B2B6B" strokeWidth="1" />
      <polygon points="16,8 24,13 24,21 16,26 8,21 8,13" fill="none" stroke="#7C3AED" strokeWidth="1.5" />
      <circle cx="16" cy="16" r="3" fill="#7C3AED" />
      <line x1="16" y1="8" x2="16" y2="13" stroke="#10B981" strokeWidth="1.5" />
      <line x1="24" y1="13" x2="19.5" y2="15.5" stroke="#10B981" strokeWidth="1.5" />
      <line x1="24" y1="21" x2="19.5" y2="18.5" stroke="#10B981" strokeWidth="1.5" />
      <line x1="16" y1="26" x2="16" y2="21" stroke="#10B981" strokeWidth="1.5" />
      <line x1="8" y1="21" x2="12.5" y2="18.5" stroke="#10B981" strokeWidth="1.5" />
      <line x1="8" y1="13" x2="12.5" y2="15.5" stroke="#10B981" strokeWidth="1.5" />
    </svg>
  );
}

export default function Sidebar({ activePage, setActivePage }: SidebarProps) {
  return (
    <aside className="fixed left-0 top-0 z-30 hidden h-screen w-64 border-r border-slate-200 bg-white/90 backdrop-blur-2xl lg:block">
      <div className="border-b border-slate-200 px-6 py-5">
        <Link href="/landing" className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/[0.04] shadow-[0_0_28px_rgba(124,58,237,0.3)]">
            <ConsensusScopeLogo />
          </div>
          <div>
            <p className="text-base font-bold text-slate-950">ConsensusScope</p>
            <p className="text-xs font-medium text-violet-600">Optimistic Democracy</p>
          </div>
        </Link>
      </div>

      <nav className="space-y-1 px-3 py-5">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.label;

          return (
            <Link
              key={item.label}
              href="/dashboard"
              onClick={() => setActivePage(item.label)}
              className={`group relative flex w-full items-center gap-3 overflow-hidden rounded-2xl px-3 py-2.5 text-sm font-semibold transition-all duration-300 ${
                isActive
              ? "bg-violet-100 text-violet-700 shadow-[0_0_28px_rgba(124,58,237,0.12)]"
                  : "text-slate-500 hover:bg-slate-100 hover:text-slate-950 hover:translate-x-1"
              }`}
            >
              {isActive ? <span className="absolute left-0 top-2 h-6 w-1 rounded-r-full bg-cyan-300" /> : null}
              <Icon size={18} />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 border-t border-slate-200 p-4">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">
            AI Validator Swarm
          </p>
          <div className="mt-3 flex items-center gap-2">
            <span className="relative flex h-2.5 w-2.5">
              <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-300 opacity-70" />
              <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-emerald-300" />
            </span>
            <span className="text-sm font-bold text-slate-950">GenLayer Ready</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
