interface PageHeadingProps {
  title: string;
  subtitle?: string;
}

export function PageHeading({ title, subtitle }: PageHeadingProps) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-bold tracking-tight text-surface-900 sm:text-3xl">
        {title}
      </h1>
      {subtitle && (
        <p className="mt-1 text-sm text-surface-500">{subtitle}</p>
      )}
    </div>
  );
}
