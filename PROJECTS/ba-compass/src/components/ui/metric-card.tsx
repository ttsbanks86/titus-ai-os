import type { KpiStatus } from "@/types";

interface MetricCardProps {
  label: string;
  value: string;
  status: KpiStatus;
}

const statusStyles: Record<KpiStatus, string> = {
  on_track: "border-green-200 bg-green-50",
  warning: "border-yellow-200 bg-yellow-50",
  critical: "border-red-200 bg-red-50",
};

const statusIcon: Record<KpiStatus, string> = {
  on_track: "●",
  warning: "●",
  critical: "●",
};

const statusColor: Record<KpiStatus, string> = {
  on_track: "text-green-600",
  warning: "text-yellow-600",
  critical: "text-red-600",
};

export function MetricCard({ label, value, status }: MetricCardProps) {
  return (
    <div
      className={`rounded-lg border p-3 ${statusStyles[status]}`}
      role="region"
      aria-label={`${label}: ${value}`}
    >
      <div className="flex items-center gap-1.5">
        <span className={`text-xs ${statusColor[status]}`} aria-hidden="true">
          {statusIcon[status]}
        </span>
        <span className="text-xs font-medium text-surface-500">{label}</span>
      </div>
      <p className={`mt-1 text-xl font-bold ${statusColor[status]}`}>
        {value}
      </p>
    </div>
  );
}
