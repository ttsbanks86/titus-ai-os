// wa-link-with-qr.mjs — Run WhatsApp login, intercept the QR string, save as PNG
import { writeFileSync, appendFileSync, existsSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve, dirname } from "node:path";
import { register } from "node:module";
import { pathToFileURL as p2f } from "node:url";

// Path to the QR terminal module
const qrTerminalPath = resolve(process.env.USERPROFILE, "AppData/Roaming/npm/node_modules/openclaw/dist/qr-terminal-zFHurnm4.js");
const mediaRuntimePath = resolve(process.env.USERPROFILE, "AppData/Roaming/npm/node_modules/openclaw/dist/plugin-sdk/media-runtime.js");

const QR_OUTPUT = "C:\\Users\\tbank\\.openclaw\\whatsapp-qr-latest.png";
const QR_DATA = "C:\\Users\\tbank\\.openclaw\\whatsapp-qr-data.txt";

console.log("=== WhatsApp Login with QR PNG ===");
console.log("QR PNG:", QR_OUTPUT);
console.log("");

// Import the SDK
const mediaSdk = await import(p2f(mediaRuntimePath).href);
const { renderQrPngBase64 } = mediaSdk;

// Monkey-patch the renderQrTerminal to also save the QR
const qrMod = await import(p2f(qrTerminalPath).href);
const originalRender = qrMod.renderQrTerminal || qrMod.default;
console.log("QR module exports:", Object.keys(qrMod));

// Use a different approach: hook into the global require
const Module = await import("node:module");
const origRequire = Module.default.prototype.require;
let qrCounter = 0;

Module.default.prototype.require = function(id) {
  const result = origRequire.apply(this, arguments);
  if (id === "openclaw/plugin-sdk/media-runtime" || id.includes("media-runtime")) {
    // Wrap the renderQrTerminal
    const orig = result.renderQrTerminal;
    if (orig && !orig._patched) {
      result.renderQrTerminal = async function(qr, opts) {
        qrCounter++;
        // Save the QR data
        writeFileSync(QR_DATA, qr);
        // Render as PNG too
        try {
          const base64 = await renderQrPngBase64(qr, { width: 600, margin: 2 });
          const buf = Buffer.from(base64, "base64");
          writeFileSync(QR_OUTPUT, buf);
          console.log(`\n[QR #${qrCounter} saved: ${buf.length} bytes to ${QR_OUTPUT}]`);
        } catch (e) {
          console.error("PNG render error:", e.message);
        }
        // Don't call the original (which prints ANSI art)
        return `[QR #${qrCounter} saved as PNG]`;
      };
      result.renderQrTerminal._patched = true;
    }
  }
  return result;
};

console.log("Patched. Starting login...");

// Now run the actual login
const { spawn } = await import("node:child_process");
const child = spawn("node", [
  resolve(process.env.USERPROFILE, "AppData/Roaming/npm/node_modules/openclaw/dist/index.js"),
  "channels", "login", "--channel", "whatsapp"
], {
  stdio: "inherit",
  env: { ...process.env, NODE_OPTIONS: "--no-warnings" }
});

child.on("close", (code) => {
  console.log(`\nLogin process exited with code ${code}`);
  if (existsSync(QR_OUTPUT)) {
    console.log(`Final QR PNG: ${QR_OUTPUT}`);
  }
  process.exit(0);
});
