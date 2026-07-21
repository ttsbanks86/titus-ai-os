interface ContentPanelProps {
  children: React.ReactNode;
  className?: string;
}

export function ContentPanel({ children, className = "" }: ContentPanelProps) {
  return (
    <div className={`rounded-lg border border-surface-200 bg-white p-4 sm:p-6 ${className}`}>
      {children}
    </div>
  );
}
