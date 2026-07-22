import Link from "next/link";
import { ContentPanel } from "@/components/ui/content-panel";
import { APP } from "@/lib/constants";

export default function NotFoundPage() {
  return (
    <div className="content-container py-16">
      <ContentPanel className="text-center">
        <div className="text-6xl font-bold text-surface-200">404</div>
        <h1 className="mt-4 text-2xl font-bold text-surface-800">Page not found</h1>
        <p className="mt-2 text-surface-500">
          This page does not exist in the {APP.NAME} case study.
        </p>
        <div className="mt-6 flex justify-center gap-3">
          <Link href="/" className="rounded-lg bg-brand-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-brand-700">
            Go home
          </Link>
          <Link href="/overview" className="rounded-lg border border-surface-300 px-5 py-2.5 text-sm font-medium text-surface-700 hover:bg-surface-50">
            View case study
          </Link>
        </div>
        <p className="mt-6 text-xs text-surface-400">
          {APP.COMPANY} is a fictional case study. All data is synthetic.
        </p>
      </ContentPanel>
    </div>
  );
}
