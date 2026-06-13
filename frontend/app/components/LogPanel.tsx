export type LogCategory = "Validators" | "Consensus" | "Security" | "GenLayer";
export type LogStatus = "success" | "error";

export interface ApiLog {
  id: string;
  timestamp: string;
  endpoint: string;
  status: LogStatus;
  category: LogCategory;
}

interface LogPanelProps {
  logs: ApiLog[];
  activeFilter: "All" | LogCategory;
  onFilterChange: (filter: "All" | LogCategory) => void;
  fullscreen?: boolean;
}

const filters: Array<"All" | LogCategory> = [
  "All",
  "Validators",
  "Consensus",
  "Security",
  "GenLayer",
];

export default function LogPanel({
  logs,
  activeFilter,
  onFilterChange,
  fullscreen = false,
}: LogPanelProps) {
  const filteredLogs =
    activeFilter === "All"
      ? logs
      : logs.filter((log) => log.category === activeFilter);

  return (
    <section className="cs-panel rounded-3xl">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-white/10 px-5 py-4">
        <div>
          <h2 className="text-lg font-bold text-white">Governance Event Log</h2>
          <p className="mt-1 text-sm text-slate-400">
            Every API call is tracked with endpoint and status.
          </p>
        </div>

        <div className="flex flex-wrap rounded-full border border-white/10 bg-white/[0.04] p-1">
          {filters.map((filter) => (
            <button
              key={filter}
              type="button"
              onClick={() => onFilterChange(filter)}
              className={`rounded-full px-3 py-1.5 text-sm font-semibold transition-colors ${
                activeFilter === filter
                  ? "bg-violet-500/20 text-violet-100"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      <div className={fullscreen ? "max-h-[620px] overflow-y-auto" : "max-h-72 overflow-y-auto"}>
        {filteredLogs.length === 0 ? (
          <div className="px-5 py-8 text-sm text-slate-400">
            No API calls recorded for this filter yet.
          </div>
        ) : (
          <div className="divide-y divide-white/10">
            {filteredLogs.map((log) => (
              <div
                key={log.id}
                className="grid gap-3 px-5 py-3 text-sm text-slate-300 md:grid-cols-[160px_1fr_120px_120px]"
              >
                <span className="font-mono text-slate-400">{log.timestamp}</span>
                <span className="font-mono font-semibold text-white">
                  {log.endpoint}
                </span>
                <span className="font-semibold text-slate-400">{log.category}</span>
                <span className="flex items-center gap-2 font-semibold capitalize text-white">
                  <span
                    className={`h-2.5 w-2.5 rounded-full ${
                      log.status === "success" ? "bg-emerald-300" : "bg-rose-300"
                    }`}
                  />
                  {log.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  );
}
