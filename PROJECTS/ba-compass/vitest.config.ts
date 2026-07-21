import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./src/tests/setup.ts"],
    include: ["src/**/*.test.{ts,tsx}", "src/tests/**/*.test.{ts,tsx}"],
    coverage: {
      reporter: ["text", "html"],
      exclude: [
        "node_modules/",
        "src/tests/setup.ts",
        "**/*.d.ts",
        "**/*.test.*",
        "**/*.config.*",
      ],
    },
  },
  esbuild: {
    jsx: "automatic",
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
