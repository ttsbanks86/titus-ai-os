const express = require("express");
const { exec } = require("child_process");
const path = require("path");
const fs = require("fs");

const app = express();
const PORT = 3737;

// Parent folder where tts-cli.js lives
const TTS_DIR = path.resolve(__dirname, "..");

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Voice lists matching tts-cli.js
const VOICES = {
  kokoro: [
    "af_sarah", "af_alloy", "af_bella", "af_nova", "af_sky",
    "am_adam", "am_echo", "am_michael", "am_liam",
    "bf_emma", "bf_isabella", "bm_george", "bm_lewis"
  ],
  edge: [
    "en-US-AriaNeural", "en-US-JennyNeural", "en-US-GuyNeural",
    "en-US-DavisNeural", "en-US-AmberNeural", "en-US-AnaNeural",
    "en-US-BrandonNeural", "en-US-ChristopherNeural", "en-US-EricNeural",
    "en-US-MichelleNeural", "en-US-MonicaNeural", "en-US-RogerNeural",
    "en-GB-SoniaNeural", "en-GB-RyanNeural", "en-AU-NatashaNeural"
  ]
};

app.get("/voices", (req, res) => {
  res.json(VOICES);
});

app.post("/generate", (req, res) => {
  const { text, voice, provider } = req.body;

  if (!text || !text.trim()) {
    return res.status(400).json({ error: "Text is required." });
  }

  const safeText = text.replace(/\\/g, "\\\\").replace(/"/g, '\\"');
  const safeVoice = voice || "af_sarah";
  const safeProvider = provider || "kokoro";
  const timestamp = Date.now();

  const cmd = `node tts-cli.js "${safeText}" ${safeVoice} ${safeProvider}`;
  console.log(`[TTS Studio] Running: ${cmd}`);

  exec(cmd, { cwd: TTS_DIR, timeout: 90000 }, (err, stdout, stderr) => {
    if (err) {
      console.error("[TTS Studio] Error:", err.message);
      return res.status(500).json({ error: "TTS generation failed.", detail: err.message });
    }

    console.log("[TTS Studio] stdout:", stdout);

    // Find the most recently modified WAV in TTS_DIR
    let files;
    try {
      files = fs.readdirSync(TTS_DIR)
        .filter(f => f.startsWith("tts-output-") && f.endsWith(".wav"))
        .map(f => ({ name: f, time: fs.statSync(path.join(TTS_DIR, f)).mtimeMs }))
        .sort((a, b) => b.time - a.time);
    } catch (e) {
      return res.status(500).json({ error: "Could not read output directory." });
    }

    if (files.length === 0) {
      return res.status(500).json({ error: "No output WAV file was created." });
    }

    const latestWav = path.join(TTS_DIR, files[0].name);
    const outputMp3 = latestWav.replace(".wav", ".mp3");

    // Try ffmpeg for MP3 — fall back to WAV if not installed
    exec(`ffmpeg -y -i "${latestWav}" -codec:a libmp3lame -qscale:a 2 "${outputMp3}"`, (ffErr) => {
      if (ffErr) {
        console.log("[TTS Studio] ffmpeg not available — serving WAV");
        const wavData = fs.readFileSync(latestWav);
        res.setHeader("Content-Type", "audio/wav");
        res.setHeader("Content-Disposition", `attachment; filename="tts-studio-${timestamp}.wav"`);
        return res.send(wavData);
      }

      const mp3Data = fs.readFileSync(outputMp3);
      res.setHeader("Content-Type", "audio/mpeg");
      res.setHeader("Content-Disposition", `attachment; filename="tts-studio-${timestamp}.mp3"`);
      res.send(mp3Data);

      // Clean up temp files
      try { fs.unlinkSync(latestWav); } catch (_) {}
      try { fs.unlinkSync(outputMp3); } catch (_) {}
    });
  });
});

app.listen(PORT, () => {
  console.log(`\n✅ TTS Studio is running!\n`);
  console.log(`   Open in browser: http://localhost:${PORT}\n`);
});
