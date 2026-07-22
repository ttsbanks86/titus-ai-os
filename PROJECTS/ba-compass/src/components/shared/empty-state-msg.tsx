interface EmptyStateMessageProps {
  title: string;
  message: string;
  action?: { label: string; href: string };
}

export function EmptyStateMessage({ title, message, action }: EmptyStateMessageProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-surface-300 bg-surface-50 px-6 py-10 text-center">
      <p className="text-sm font-medium text-surface-600">{title}</p>
      <p className="mt-1 max-w-md text-xs text-surface-400">{message}</p>
      {action && (
        <a href={action.href} className="mt-3 rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-brand-700">
          {action.label}
        </a>
      )}
    </div>
  );
}
