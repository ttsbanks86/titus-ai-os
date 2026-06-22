const sharp = require("sharp");
const path = require("path");

const svg = `<svg width="512" height="512" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="512" y2="512" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#1a0f3c"/>
    <stop offset="100%" stop-color="#0a0a18"/>
  </linearGradient>
  <linearGradient id="micG" x1="0" y1="120" x2="0" y2="298" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#7c3aed"/>
    <stop offset="100%" stop-color="#4c1d95"/>
  </linearGradient>
  <linearGradient id="standG" x1="0" y1="250" x2="0" y2="390" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#a78bfa"/>
    <stop offset="100%" stop-color="#6d28d9"/>
  </linearGradient>
  <linearGradient id="shine" x1="0" y1="0" x2="512" y2="512" gradientUnits="userSpaceOnUse">
    <stop offset="0%" stop-color="#ffffff" stop-opacity="0.13"/>
    <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
  </linearGradient>
  <clipPath id="clip">
    <rect x="0" y="0" width="512" height="512" rx="100" ry="100"/>
  </clipPath>
</defs>

<rect x="0" y="0" width="512" height="512" rx="100" fill="url(#bg)"/>
<rect x="0" y="0" width="512" height="512" rx="100" fill="none" stroke="#3b1f7a" stroke-width="2"/>
<rect x="0" y="0" width="512" height="512" rx="100" fill="url(#shine)"/>

<g clip-path="url(#clip)">
  <circle cx="256" cy="248" r="166" fill="none" stroke="#4c1d95" stroke-width="2" stroke-dasharray="5 7"/>
  <circle cx="256" cy="248" r="132" fill="none" stroke="#5b21b6" stroke-width="1.5" stroke-dasharray="3 7"/>

  <path d="M 148 158 Q 112 248 148 338" fill="none" stroke="#7c3aed" stroke-width="6" stroke-linecap="round" opacity="0.75"/>
  <path d="M 172 184 Q 144 248 172 312" fill="none" stroke="#a78bfa" stroke-width="4" stroke-linecap="round" opacity="0.45"/>
  <path d="M 364 158 Q 400 248 364 338" fill="none" stroke="#7c3aed" stroke-width="6" stroke-linecap="round" opacity="0.75"/>
  <path d="M 340 184 Q 368 248 340 312" fill="none" stroke="#a78bfa" stroke-width="4" stroke-linecap="round" opacity="0.45"/>

  <rect x="218" y="118" width="78" height="136" rx="39" fill="url(#micG)"/>
  <rect x="228" y="130" width="28" height="64" rx="14" fill="#a78bfa" opacity="0.22"/>
  <line x1="232" y1="168" x2="280" y2="168" stroke="#c4b5fd" stroke-width="2" stroke-linecap="round" opacity="0.55"/>
  <line x1="228" y1="185" x2="284" y2="185" stroke="#c4b5fd" stroke-width="2" stroke-linecap="round" opacity="0.45"/>
  <line x1="228" y1="202" x2="284" y2="202" stroke="#c4b5fd" stroke-width="2" stroke-linecap="round" opacity="0.35"/>
  <line x1="232" y1="219" x2="280" y2="219" stroke="#c4b5fd" stroke-width="1.5" stroke-linecap="round" opacity="0.25"/>
  <line x1="238" y1="234" x2="274" y2="234" stroke="#c4b5fd" stroke-width="1.5" stroke-linecap="round" opacity="0.18"/>

  <path d="M 192 256 Q 192 330 256 330 Q 320 330 320 256" fill="none" stroke="url(#standG)" stroke-width="8" stroke-linecap="round"/>
  <line x1="256" y1="330" x2="256" y2="376" stroke="url(#standG)" stroke-width="8" stroke-linecap="round"/>
  <rect x="210" y="374" width="92" height="14" rx="7" fill="url(#standG)"/>
  <rect x="226" y="386" width="60" height="10" rx="5" fill="#4c1d95" opacity="0.75"/>

  <circle cx="256" cy="132" r="13" fill="#ede9fe" opacity="0.12"/>
  <circle cx="256" cy="132" r="6" fill="#c4b5fd" opacity="0.65"/>
</g>
</svg>`;

const outPath = path.join(__dirname, "icon.png");

sharp(Buffer.from(svg))
  .resize(512, 512)
  .png()
  .toFile(outPath)
  .then(() => console.log("icon.png written to", outPath))
  .catch(err => console.error("Error:", err));
