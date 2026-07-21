interface SectionHeadingProps {
  title: string;
  description?: string;
}

export function SectionHeading({ title, description }: SectionHeadingProps) {
  return (
    <div className="mb-4">
      <h2 className="text-lg font-semibold text-surface-800">{title}</h2>
      {description && (
        <p className="mt-0.5 text-sm text-surface-500">{description}</p>
      )}
    </div>
  );
}
