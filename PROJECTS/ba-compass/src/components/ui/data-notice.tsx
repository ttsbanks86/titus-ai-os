import { SYNTHETIC_NOTICE } from "@/lib/constants";

export function DataNotice() {
  return (
    <div
      className="rounded-lg border border-yellow-200 bg-yellow-50 px-4 py-2 text-xs text-yellow-800"
      role="note"
      aria-label="Data notice"
    >
      {SYNTHETIC_NOTICE}
    </div>
  );
}
