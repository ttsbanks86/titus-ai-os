"use client";

import { useState } from "react";
import { AlertTriangle } from "lucide-react";

interface DemoResetProps {
  onReset: () => void;
  label?: string;
}

export function DemoReset({ onReset, label = "Reset Demo Data" }: DemoResetProps) {
  const [confirming, setConfirming] = useState(false);
  const [done, setDone] = useState(false);

  const handleReset = () => {
    onReset();
    setConfirming(false);
    setDone(true);
    setTimeout(() => setDone(false), 3000);
  };

  return (
    <div className="no-print">
      {!confirming && !done && (
        <button
          onClick={() => setConfirming(true)}
          className="rounded-lg border border-red-200 bg-white px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50"
          aria-label={label}
        >
          {label}
        </button>
      )}
      {confirming && (
        <div className="flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700" role="alert">
          <AlertTriangle className="h-3.5 w-3.5 shrink-0" />
          <span>Reset all demo data to original state? This clears local edits.</span>
          <button onClick={handleReset} className="rounded bg-red-600 px-2 py-1 text-xs font-medium text-white hover:bg-red-700">Reset</button>
          <button onClick={() => setConfirming(false)} className="rounded bg-white px-2 py-1 text-xs font-medium text-surface-600 hover:bg-surface-100">Cancel</button>
        </div>
      )}
      {done && (
        <div className="rounded-lg border border-green-200 bg-green-50 px-3 py-2 text-xs text-green-700" role="status">
          Demo data has been reset.
        </div>
      )}
    </div>
  );
}
