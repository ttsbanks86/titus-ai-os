"use client";

import { useState } from "react";
import Link from "next/link";
import { Menu, X } from "lucide-react";
import { APP, NAV_ITEMS } from "@/lib/constants";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-surface-200 bg-white">
      <div className="content-container flex h-14 items-center justify-between">
        {/* Logo / Title */}
        <Link href="/" className="flex items-center gap-2 text-sm font-semibold text-surface-800">
          <span className="flex h-7 w-7 items-center justify-center rounded bg-brand-600 text-xs font-bold text-white">
            BA
          </span>
          <span className="hidden sm:inline">{APP.NAME}</span>
        </Link>

        {/* Desktop Navigation */}
        <nav className="hidden lg:block" aria-label="Main navigation">
          <ul className="flex items-center gap-1">
            {NAV_ITEMS.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  className="rounded-md px-2.5 py-1.5 text-sm text-surface-600 transition-colors hover:bg-surface-100 hover:text-surface-800"
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        {/* Mobile toggle */}
        <button
          type="button"
          className="inline-flex items-center justify-center rounded-md p-2 text-surface-500 hover:bg-surface-100 hover:text-surface-700 lg:hidden"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-expanded={mobileOpen}
          aria-controls="mobile-menu"
          aria-label={mobileOpen ? "Close menu" : "Open menu"}
        >
          {mobileOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Navigation Drawer */}
      {mobileOpen && (
        <nav
          id="mobile-menu"
          className="border-t border-surface-200 bg-white lg:hidden"
          aria-label="Mobile navigation"
        >
          <ul className="content-container divide-y divide-surface-100 py-2">
            {NAV_ITEMS.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  className="block px-2 py-3 text-sm text-surface-700 hover:text-brand-600"
                  onClick={() => setMobileOpen(false)}
                >
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </header>
  );
}
