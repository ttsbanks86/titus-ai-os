// wa-qr-link.mjs — Generate WhatsApp QR PNG without using the terminal
// Hooks into the OpenClaw WhatsApp plugin to get the QR string,
// then renders it as a PNG using the plugin's own renderQrPngDataUrl

import { writeFileSync, existsSync } from "node:fs";
import { spawn } from "node:child_process";
import path from "node:path";

// Import the SDK
const sdkPath = "C:\\Users\\tbank\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\plugin-sdk\\media-runtime.js";
const { renderQrPngDataUrl } = await import("file:///" + sdkPath.replace(/\\/g, "/"));

const OUTPUT = "C:\\Users\\tbank\\Desktop\\whatsapp-qr.png";
const FRESH_OUTPUT = "C:\\Users\\tbank\\Desktop\\whatsapp-qr-latest.png";

let qrCount = 0;

console.log("=== WhatsApp QR Generator ===");
console.log("Starting WhatsApp login...");
console.log("Will save QR to:", OUTPUT);
console.log("");

// Spawn the login command
const child = spawn("node", [
  "C:\\Users\\tbank\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\index.js",
  "channels", "login", "--channel", "whatsapp"
], {
  stdio: ["ignore", "pipe", "pipe"]
});

let qrBuffer = "";
let isWaiting = true;

child.stdout.on("data", async (data) => {
  const text = data.toString("utf8");
  // Strip ANSI codes
  const clean = text.replace(/\x1b\[[0-9;]*m/g, "").replace(/\r/g, "");
  qrBuffer += clean;
  process.stdout.write(text);
  
  // Check if we see the QR prompt
  if (isWaiting && clean.includes("scan this QR")) {
    isWaiting = false;
    console.log("\n\n[QR DETECTED - waiting for next QR refresh]");
  }
});

child.stderr.on("data", (data) => {
  process.stderr.write(data);
});

child.on("close", (code) => {
  console.log(`\n\nLogin process exited with code ${code}`);
  console.log(`Total QRs captured: ${qrCount}`);
});

// We can't easily intercept the actual QR string from the spawned process
// So this approach won't work as-is. Let me try a different method.
setTimeout(() => {
  console.log("\n[Note: This approach can't intercept the QR string from the spawned process.]");
  console.log("[Need to use the plugin SDK directly to hook into onQr]");
  child.kill();
  process.exit(0);
}, 30000);
