export function LoadingSkeleton({ lines = 3 }: { lines?: number }) {
  return (
    <div className="animate-pulse space-y-3" role="status" aria-label="Loading content">
      <div className="h-4 w-3/4 rounded bg-surface-200" />
      {Array.from({ length: lines }).map((_, i) => (
        <div key={i} className="h-3 rounded bg-surface-100" style={{ width: `${85 - i * 10}%` }} />
      ))}
      <span className="sr-only">Loading...</span>
    </div>
  );
}
