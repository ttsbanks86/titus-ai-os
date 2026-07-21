import type { Metadata, Viewport } from "next";
import "./globals.css";
import { APP, SYNTHETIC_NOTICE } from "@/lib/constants";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";

export const metadata: Metadata = {
  title: {
    default: `${APP.NAME} — ${APP.SUBTITLE}`,
    template: `%s — ${APP.NAME}`,
  },
  description: APP.DESCRIPTION,
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
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

        <main id="main-content" className="flex-1">
          {children}
        </main>

        <Footer />
      </body>
    </html>
  );
}
