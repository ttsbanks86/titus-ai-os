interface TableWrapperProps {
  children: React.ReactNode;
  caption?: string;
}

export function TableWrapper({ children, caption }: TableWrapperProps) {
  return (
    <div className="overflow-x-auto rounded-lg border border-surface-200">
      <table className="min-w-full divide-y divide-surface-200 text-sm">
        {caption && (
          <caption className="sr-only">{caption}</caption>
        )}
        {children}
      </table>
    </div>
  );
}
