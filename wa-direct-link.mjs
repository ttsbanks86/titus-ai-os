// wa-direct-link.mjs — Use Baileys directly to get the QR as a PNG
// This bypasses the OpenClaw login CLI entirely
import { writeFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

// Use absolute path to baileys
const baileysPath = resolve(process.env.USERPROFILE, ".openclaw/extensions/whatsapp/node_modules/baileys/lib/index.js");
const { default: makeWASocket, useMultiFileAuthState, DisconnectReason } = await import(pathToFileURL(baileysPath).href);
import qrcode from "qrcode";
import qrcodeTerminal from "qrcode-terminal";
import { Boom } from "@hapi/boom";

const AUTH_DIR = "C:\\Users\\tbank\\.openclaw\\whatsapp-auth-tmp";
const QR_PNG = "C:\\Users\\tbank\\Desktop\\whatsapp-qr.png";

console.log("=== WhatsApp Direct Link ===");
console.log("Auth dir:", AUTH_DIR);
console.log("QR PNG output:", QR_PNG);
console.log("");

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  
  const sock = makeWASocket({
    auth: state,
    printQRInTerminal: false,  // we'll handle the QR ourselves
    logger: { level: 'silent', child: () => ({ level: 'silent' }), info: () => {}, warn: () => {}, error: () => {}, debug: () => {}, trace: () => {} }
  });
  
  let qrCount = 0;
  
  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect, qr } = update;
    
    if (qr) {
      qrCount++;
      console.log(`\n[QR #${qrCount} received - saving as PNG...]`);
      
      // Render as PNG
      try {
        const pngBuffer = await qrcode.toBuffer(qr, { width: 600, margin: 2 });
        writeFileSync(QR_PNG, pngBuffer);
        console.log("[QR saved to Desktop]");
        
        // Also show in terminal
        qrcodeTerminal.generate(qr, { small: true });
        
        console.log("\n>>> SCAN THIS QR WITH YOUR WHATSAPP APP <<<");
        console.log(">>> Open WhatsApp > Linked Devices > Link a Device <<<");
        console.log(">>> OR open the PNG file at the path above <<<");
      } catch (e) {
        console.error("Error saving QR:", e.message);
      }
    }
    
    if (connection === "close") {
      const reason = new Boom(lastDisconnect?.error)?.output?.statusCode;
      console.log("Connection closed. Reason:", reason);
      
      if (reason === DisconnectReason.loggedOut) {
        console.log("Logged out. Delete the auth dir and re-link.");
        process.exit(0);
      } else {
        console.log("Reconnecting in 5s...");
        setTimeout(start, 5000);
      }
    } else if (connection === "open") {
      console.log("\n[CONNECTED! WhatsApp linked successfully.]");
      console.log("[Saving credentials and exiting...]");
      await saveCreds();
      process.exit(0);
    }
  });
  
  sock.ev.on("creds.update", saveCreds);
}

start().catch(e => {
  console.error("Fatal:", e.message);
  process.exit(1);
});

// Keep alive
setInterval(() => {}, 60000);

