interface EmptyStateProps {
  title: string;
  description?: string;
}

export function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border border-dashed border-surface-300 bg-surface-50 p-8 text-center">
      <p className="text-sm font-medium text-surface-600">{title}</p>
      {description && (
        <p className="mt-1 text-xs text-surface-400">{description}</p>
      )}
    </div>
  );
}
