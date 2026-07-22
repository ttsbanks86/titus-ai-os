"use client";

import React from "react";
import Link from "next/link";
import { ContentPanel } from "@/components/ui/content-panel";

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="content-container py-8">
          <ContentPanel>
            <h2 className="text-lg font-semibold text-surface-800">Something went wrong</h2>
            <p className="mt-2 text-sm text-surface-600">
              This section encountered an unexpected error. Please try reloading the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="mt-3 rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
            >
              Reload page
            </button>
            <Link href="/" className="ml-2 mt-3 inline-block rounded-lg border border-surface-300 px-4 py-2 text-sm font-medium text-surface-700 hover:bg-surface-50">
              Go home
            </Link>
          </ContentPanel>
        </div>
      );
    }
    return this.props.children;
  }
}
