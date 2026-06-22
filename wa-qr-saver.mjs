// wa-qr-saver.mjs — Try multiple import paths
import { writeFileSync } from "node:fs";
import path from "node:path";

async function main() {
  // Try the plugin's own node_modules first
  const candidates = [
    "C:\\Users\\tbank\\.openclaw\\extensions\\whatsapp\\node_modules\\openclaw\\plugin-sdk\\media-runtime.js",
    "C:\\Users\\tbank\\AppData\\Roaming\\npm\\node_modules\\openclaw\\dist\\plugin-sdk\\media-runtime.js",
  ];
  
  for (const p of candidates) {
    try {
      const mod = await import(pathToFileUrl(p));
      console.log("Loaded:", p);
      if (mod.renderQrPngDataUrl) {
        const dataUrl = await mod.renderQrPngDataUrl("https://example.com/test");
        const base64 = dataUrl.replace(/^data:image\/png;base64,/, "");
        writeFileSync("C:\\Users\\tbank\\Desktop\\whatsapp-test-qr.png", base64, "base64");
        console.log("Saved test QR");
        return;
      }
    } catch (e) {
      console.log("Failed:", p, "-", e.message);
    }
  }
  console.log("No working import found");
}

function pathToFileUrl(p) {
  return "file:///" + p.replace(/\\/g, "/");
}

main();
