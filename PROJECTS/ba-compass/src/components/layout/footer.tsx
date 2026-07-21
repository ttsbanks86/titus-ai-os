import { APP } from "@/lib/constants";

export function Footer() {
  return (
    <footer className="border-t border-surface-200 bg-white py-6">
      <div className="content-container">
        <div className="flex flex-col items-center justify-between gap-2 text-center text-xs text-surface-400 sm:flex-row sm:text-left">
          <p>
            {APP.NAME} — {APP.SUBTITLE}
          </p>
          <p>
            {APP.COMPANY} is a fictional case study. All data is synthetic.
          </p>
        </div>
      </div>
    </footer>
  );
}
