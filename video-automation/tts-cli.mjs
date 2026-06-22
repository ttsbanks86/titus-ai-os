#!/usr/bin/env node
/**
 * Unified TTS CLI
 * Usage: node tts-cli.mjs "Text to speak" [voice] [provider]
 */

import { UnifiedTTS } from "./src/tts.js";

async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
Unified TTS CLI

Usage:
  node tts-cli.mjs "Text to speak" [voice] [provider]

Providers:
  auto      - Auto-select (offline first) [default]
  supertonic - Supertonic TTS (10 voices, 31 languages)
  kokoro    - Kokoro-ONNX (26 voices, 646+ languages)
  edge      - Edge TTS (online, requires internet)

Voices:
  Supertonic: F1-F5, M1-M5
  Kokoro: af_sarah, af_alloy, af_bella, af_nova, af_sky, am_adam, am_echo, etc.
  Edge: en-US-AriaNeural, en-US-JennyNeural, en-US-GuyNeural, etc.

Examples:
  node tts-cli.mjs "Hello world"
  node tts-cli.mjs "Hello world" F1 supertonic
  node tts-cli.mjs "Hello world" af_sarah kokoro
  node tts-cli.mjs "Hello world" en-US-AriaNeural edge
`);
    process.exit(0);
  }

  const text = args[0];
  const voice = args[1] || "F1";
  const provider = (args[2] as "auto" | "supertonic" | "kokoro" | "edge") || "auto";

  const tts = await import("./src/tts.js");
  const ttsInstance = new tts.UnifiedTTS();
  await ttsInstance.initialize();

  const outputPath = `./tts-output-${Date.now()}.wav`;
  
  console.log(`[TTS] Provider: ${provider}, Voice: ${voice}`);
  console.log(`[TTS] Text: "${text}"`);
  
  const result = await tts.UnifiedTTS.prototype.speak.call(
    await import("./src/tts.js").then(m => new m.UnifiedTTS()),
    text,
    { provider: provider as any, voice }
  );

  console.log("Result:", result);
}

main().catch(console.error);