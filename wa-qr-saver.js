// wa-qr-saver.js — Hook into the WhatsApp login and save QR as PNG
// Uses the plugin's renderQrPngDataUrl which we know exists
const path = require('path');

async function main() {
  const waPlugin = require(path.join(process.env.USERPROFILE, '.openclaw/extensions/whatsapp/dist/index.js'));
  console.log('Plugin keys:', Object.keys(waPlugin).slice(0, 20));
  
  // Try to find the QR function
  for (const [name, fn] of Object.entries(waPlugin)) {
    if (typeof fn === 'function' && (name.includes('Qr') || name.includes('qr') || name.includes('Login'))) {
      console.log(`Found: ${name}`);
    }
  }
}

main().catch(e => console.error('Error:', e.message));
