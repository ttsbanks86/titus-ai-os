// wa-qr-only.mjs — Use OpenClaw's own SDK to render a QR PNG
// We need to get a QR string from somewhere - test with a placeholder first
import { writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

// Use absolute path to the SDK
const sdkPath = resolve(process.env.USERPROFILE, "AppData/Roaming/npm/node_modules/openclaw/dist/plugin-sdk/media-runtime.js");
const sdk = await import(pathToFileURL(sdkPath).href);

const { writeQrPngTempFile, renderQrPngBase64 } = sdk;

console.log("=== OpenClaw QR PNG Generator ===");

// Test: render a placeholder
try {
  const result = await writeQrPngTempFile("https://example.com/test-qr-from-openclaw-sdk", {
    dirPrefix: "qr-test",
    fileName: "test-qr.png",
    tmpRoot: "C:\\Users\\tbank\\AppData\\Local\\Temp"
  });
  console.log("Test QR written to:", result.filePath);
  console.log("Bytes:", result.bytes);
  
  // Also save a copy to Desktop
  const fs = await import("node:fs");
  fs.copyFileSync(result.filePath, "C:\\Users\\tbank\\Desktop\\openclaw-test-qr.png");
  console.log("Copied to Desktop as openclaw-test-qr.png");
  
  // Test renderQrPngBase64 directly
  const base64 = await renderQrPngBase64("https://example.com/test");
  console.log("Base64 length:", base64.length);
} catch (e) {
  console.error("Error:", e.message, e.stack);
}
