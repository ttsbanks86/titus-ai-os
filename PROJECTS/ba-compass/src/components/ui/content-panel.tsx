interface ContentPanelProps {
  children: React.ReactNode;
  className?: string;
  id?: string;
  printHide?: boolean;
}

export function ContentPanel({ children, className = "", id, printHide }: ContentPanelProps) {
  return (
    <div
      id={id}
      className={`rounded-lg border border-surface-200 bg-white p-4 sm:p-6 ${printHide ? "no-print" : ""} ${className}`}
    >
      {children}
    </div>
  );
}
