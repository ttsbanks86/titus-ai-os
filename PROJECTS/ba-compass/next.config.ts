import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export ready for Vercel deployment
  output: "export",

  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },

  // Strict mode for development quality
  reactStrictMode: true,
};

export default nextConfig;
