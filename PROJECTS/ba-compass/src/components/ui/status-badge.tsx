interface StatusBadgeProps {
  label: string;
  variant?: "success" | "warning" | "error" | "info" | "neutral";
}

export function StatusBadge({ label, variant = "neutral" }: StatusBadgeProps) {
  const classMap = {
    success: "status-badge--success",
    warning: "status-badge--warning",
    error: "status-badge--error",
    info: "status-badge--info",
    neutral: "status-badge--neutral",
  };

  return (
    <span className={`status-badge ${classMap[variant]}`}>
      {label}
    </span>
  );
}
