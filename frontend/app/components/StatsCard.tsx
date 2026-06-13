import type { LucideIcon } from "lucide-react";

interface StatsCardProps {
  label: string;
  value: string;
  indicator: string;
  icon: LucideIcon;
}

export default function StatsCard({ label, value, indicator, icon: Icon }: StatsCardProps) {
  return (
    <article className="cs-panel cs-panel-hover rounded-3xl p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-400">{label}</p>
          <p className="mt-3 text-3xl font-black text-slate-950">{value}</p>
        </div>
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-violet-200 bg-violet-50 text-violet-600">
          <Icon size={20} />
        </div>
      </div>
      <p className="mt-4 text-sm font-semibold text-emerald-600">{indicator}</p>
    </article>
  );
}
