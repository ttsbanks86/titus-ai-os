import type { Metadata, Viewport } from "next";
import "./globals.css";
import { APP, SYNTHETIC_NOTICE } from "@/lib/constants";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
import { RequirementsProvider } from "@/lib/state/requirements-store";

export const metadata: Metadata = {
  title: {
    default: `${APP.NAME} — ${APP.SUBTITLE}`,
    template: `%s — ${APP.NAME}`,
  },
  description: APP.DESCRIPTION,
  openGraph: {
    title: `${APP.NAME} — Business Analyst Portfolio Case Study`,
    description: "A recruiter-ready BA portfolio demonstrating end-to-end business analysis through a fictional home-care services case study.",
    type: "website",
    siteName: APP.NAME,
  },
  twitter: {
    card: "summary_large_image",
    title: `${APP.NAME} — BA Portfolio Case Study`,
    description: APP.DESCRIPTION,
  },
  robots: {
    index: false,
    follow: false,
  },
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#2563eb",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen flex-col">
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>

        <div className="notice-bar" role="note" aria-label="Synthetic data notice">
          {SYNTHETIC_NOTICE}
        </div>

        <Header />

        <RequirementsProvider>
          <main id="main-content" className="flex-1">
            {children}
          </main>
        </RequirementsProvider>

        <Footer />
      </body>
    </html>
  );
}
