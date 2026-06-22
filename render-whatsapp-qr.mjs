// render-whatsapp-qr.mjs — Convert the captured QR data to a PNG
import { writeFileSync, readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

const sdkPath = resolve(process.env.USERPROFILE, "AppData/Roaming/npm/node_modules/openclaw/dist/plugin-sdk/media-runtime.js");
const { renderQrPngBase64, writeQrPngTempFile } = await import(pathToFileURL(sdkPath).href);

const qrData = readFileSync("C:\\Users\\tbank\\.openclaw\\wa-qr-captured.txt", "utf8").trim();
console.log("Rendering QR for data:", qrData.substring(0, 60), "...");
console.log("Data length:", qrData.length);

try {
  const result = await writeQrPngTempFile(qrData, {
    dirPrefix: "whatsapp-qr",
    fileName: "whatsapp-qr.png",
    tmpRoot: "C:\\Users\\tbank\\Desktop"
  });
  console.log("Saved to:", result.filePath);
  // Also copy with a clear name
  const fs = await import("node:fs");
  fs.copyFileSync(result.filePath, "C:\\Users\\tbank\\Desktop\\SCAN-THIS-FOR-WHATSAPP.png");
  console.log("Copied to: C:\\Users\\tbank\\Desktop\\SCAN-THIS-FOR-WHATSAPP.png");
} catch (e) {
  console.error("Error:", e.message);
}
