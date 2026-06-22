/**
 * Video Automation Pipeline
 *
 * 1. Read transcript
 * 2. Generate timed captions (estimated from speaking rate)
 * 3. Extract keywords for b-roll
 * 4. Search Pixabay API for matching clips
 * 5. Download b-roll clips
 * 6. Render final video via Remotion
 *
 * Usage:
 *   node scripts/run-pipeline.mjs --video "path/to/video.mp4" --transcript "path/to/transcript.txt"
 */

import { execSync, spawn } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import https from "https";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, "..");

// ── Config ───────────────────────────────────────────────────
const PIXABAY_API_KEY = process.env.PIXABAY_API_KEY || "56137839-54677f318092fc44bea5dd100";
const FPS = 30;
const WORDS_PER_MINUTE = 150;
const MAX_B_ROLL_CLIPS = 3;
const B_ROLL_DIR = path.join(PROJECT_ROOT, "b-roll");
const OUTPUT_DIR = path.join(PROJECT_ROOT, "output");
const INPUT_DIR = path.join(PROJECT_ROOT, "input");

// ── Helpers ──────────────────────────────────────────────────

function parseArgs() {
  const args = {};
  process.argv.slice(2).forEach((arg, i, arr) => {
    if (arg.startsWith("--")) {
      const key = arg.slice(2);
      const val = arr[i + 1] && !arr[i + 1].startsWith("--") ? arr[i + 1] : true;
      args[key] = val;
    }
  });
  return args;
}

function estimateCaptions(text, totalDurationMs) {
  // Split text into sentences
  const sentences = text
    .replace(/\n+/g, " ")
    .split(/[.!?]+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

  const totalWords = text.split(/\s+/).length;
  const estimatedMs = (totalWords / WORDS_PER_MINUTE) * 60 * 1000;
  const durationMs = totalDurationMs || estimatedMs;

  // Distribute sentences across the duration
  const totalChars = sentences.reduce((sum, s) => sum + s.length, 0);
  let currentMs = 500; // start 0.5s in
  const captions = [];

  for (const sentence of sentences) {
    const proportion = sentence.length / totalChars;
    const sentenceDuration = Math.max(1500, proportion * durationMs);
    const endMs = Math.min(currentMs + sentenceDuration, durationMs - 500);
    captions.push({
      startMs: Math.round(currentMs),
      endMs: Math.round(endMs),
      text: sentence + ".",
    });
    currentMs = endMs + 100; // small gap
  }

  return { captions, durationMs };
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { "User-Agent": "Mozilla/5.0" } }, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`JSON parse error: ${data.slice(0, 200)}`));
        }
      });
    }).on("error", reject);
  });
}

function downloadFile(url, dest) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(dest);
    https.get(url, { headers: { "User-Agent": "Mozilla/5.0" } }, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`Download failed: ${res.statusCode}`));
        return;
      }
      res.pipe(file);
      file.on("finish", () => {
        file.close();
        resolve(dest);
      });
    }).on("error", (err) => {
      fs.unlinkSync(dest);
      reject(err);
    });
  });
}

function getVideoDuration(videoPath) {
  try {
    const output = execSync(
      `ffprobe -v error -show_entries format=duration -of csv=p=0 "${videoPath}"`,
      { encoding: "utf-8", timeout: 15000 }
    );
    return parseFloat(output.trim()) * 1000; // ms
  } catch (e) {
    console.warn("Could not get video duration, estimating from transcript...");
    return null;
  }
}

// ── Step 1: Extract keywords from transcript ────────────────

function extractKeywords(text) {
  // Simple keyword extraction: find meaningful words (nouns, topics)
  const stopWords = new Set([
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "here", "there", "when", "where", "why", "how", "all", "each",
    "every", "both", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "because", "but", "and", "or", "if", "while", "that", "this",
    "these", "those", "it", "its", "you", "your", "i", "me", "my", "we",
    "our", "they", "them", "their", "he", "she", "him", "her", "his",
    "what", "which", "who", "whom", "whose", "about", "up", "down"
  ]);

  const words = text
    .toLowerCase()
    .replace(/[^a-z\s]/g, "")
    .split(/\s+/)
    .filter((w) => w.length > 3 && !stopWords.has(w));

  // Count frequency
  const freq = {};
  words.forEach((w) => (freq[w] = (freq[w] || 0) + 1));

  // Sort by frequency, take top 5 unique keywords
  return Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([word]) => word);
}

// ── Step 2: Search Pixabay for b-roll ────────────────────────

async function searchPixabayVideos(keywords, count = MAX_B_ROLL_CLIPS) {
  const results = [];
  const usedKeywords = [];

  for (const keyword of keywords) {
    if (results.length >= count) break;
    if (usedKeywords.includes(keyword)) continue;
    usedKeywords.push(keyword);

    console.log(`  Searching Pixabay for: "${keyword}"...`);
    try {
      const url = `https://pixabay.com/api/videos/?key=${PIXABAY_API_KEY}&q=${encodeURIComponent(keyword)}&per_page=3&safesearch=true`;
      const data = await fetchJson(url);

      if (data.hits && data.hits.length > 0) {
        const hit = data.hits[0];
        // Get the smallest video (tiny) for faster download
        const videos = hit.videos;
        const videoUrl = videos.small?.url || videos.tiny?.url || videos.medium?.url;
        if (videoUrl) {
          results.push({ keyword, url: videoUrl, duration: hit.duration });
          console.log(`    Found clip: ${videoUrl}`);
        }
      }
    } catch (e) {
      console.warn(`    Error searching for "${keyword}": ${e.message}`);
    }
  }

  return results;
}

// ── Step 3: Download b-roll clips ────────────────────────────

async function downloadBRoll(clips) {
  const downloaded = [];
  for (let i = 0; i < clips.length; i++) {
    const clip = clips[i];
    const ext = path.extname(clip.url) || ".mp4";
    const dest = path.join(B_ROLL_DIR, `broll_${i}${ext}`);
    const publicDest = path.join(PROJECT_ROOT, "public", `broll_${i}${ext}`);
    console.log(`  Downloading b-roll ${i + 1}/${clips.length}: ${clip.keyword}...`);
    try {
      await downloadFile(clip.url, dest);
      // Copy to public/ for Remotion staticFile access
      fs.copyFileSync(dest, publicDest);
      downloaded.push({ ...clip, filePath: dest, publicName: `broll_${i}${ext}` });
      console.log(`    Saved to: ${dest}`);
    } catch (e) {
      console.warn(`    Failed to download: ${e.message}`);
    }
  }
  return downloaded;
}

// ── Music search on Pixabay ──────────────────────────────────

async function searchPixabayMusic(query = "ambient inspirational") {
  console.log(`  Searching Pixabay music for: "${query}"...`);
  // Pixabay music API endpoint; falls back gracefully if unavailable
  try {
    const url = `https://pixabay.com/api/music/?key=${PIXABAY_API_KEY}&q=${encodeURIComponent(query)}&per_page=5`;
    console.log(`    Fetching: ${url.replace(PIXABAY_API_KEY, "***")}`);
    const data = await fetchJson(url);
    if (data.hits && data.hits.length > 0) {
      for (const hit of data.hits) {
        const audioUrl = hit.audio_url || hit.preview_url || hit.url;
        if (audioUrl) {
          const title = hit.title || "background";
          console.log(`    Found track: "${title}"`);
          return { url: audioUrl, title, duration: hit.duration || 30 };
        }
      }
    }
    console.warn("    No music found on Pixabay");
    return null;
  } catch (e) {
    console.warn(`    Music search error (non-critical): ${e.message}`);
    // Try alternate approach: use Pixabay video API with "music" or "background" query
    // and extract just the audio... or just skip music
    console.log("    Skipping background music (optional feature)");
    return null;
  }
}

// ── Step 4: Generate SRT captions ────────────────────────────

function generateSRT(captions) {
  function formatTime(ms) {
    const totalSec = ms / 1000;
    const h = Math.floor(totalSec / 3600);
    const m = Math.floor((totalSec % 3600) / 60);
    const s = Math.floor(totalSec % 60);
    const msPart = Math.floor((totalSec % 1) * 1000);
    return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")},${String(msPart).padStart(3, "0")}`;
  }

  return captions
    .map((c, i) => {
      return `${i + 1}\n${formatTime(c.startMs)} --> ${formatTime(c.endMs)}\n${c.text}\n`;
    })
    .join("\n");
}

// ── Step 5: Render video with Remotion ───────────────────────

async function renderVideo(mainVideoPath, captions, bRollClips, outputPath, musicInfo = null) {
  console.log("  Rendering final video with Remotion...");

  const publicDir = path.join(PROJECT_ROOT, "public");
  fs.mkdirSync(publicDir, { recursive: true });

  // Copy main video to public/ for Remotion staticFile access
  const mainVideoExt = path.extname(mainVideoPath);
  const publicMainName = `input${mainVideoExt}`;
  fs.copyFileSync(mainVideoPath, path.join(publicDir, publicMainName));

  // Download background music if available
  let publicMusicName = null;
  let musicVolume = 0.12; // default: quiet background
  if (musicInfo && musicInfo.url) {
    const musicExt = ".mp3";
    const musicDest = path.join(PROJECT_ROOT, "b-roll", `background_music${musicExt}`);
    publicMusicName = `background_music${musicExt}`;
    const musicPublicDest = path.join(publicDir, publicMusicName);
    try {
      console.log(`  Downloading background music: ${musicInfo.title}...`);
      await downloadFile(musicInfo.url, musicDest);
      fs.copyFileSync(musicDest, musicPublicDest);
      console.log(`    Music saved to: ${musicDest}`);
    } catch (e) {
      console.warn(`    Music download failed: ${e.message}`);
      publicMusicName = null;
    }
  }

  // Distribute b-roll clips across the timeline
  const bRollDeploy = [];
  if (bRollClips.length > 0) {
    const captionsDuration = captions.length > 0
      ? captions[captions.length - 1].endMs
      : 30000;
    const gap = captionsDuration / (bRollClips.length + 1);
    bRollClips.forEach((c, i) => {
      bRollDeploy.push({
        src: c.publicName,
        startMs: Math.round(gap * (i + 1)),
        durationMs: Math.min(c.duration ? c.duration * 1000 : 4000, 6000),
      });
    });
  }

  // Build the input props JSON
  const inputProps = {
    mainVideoSrc: publicMainName,
    captions: captions.map((c) => ({
      startMs: c.startMs,
      endMs: c.endMs,
      text: c.text,
    })),
    bRollClips: bRollDeploy,
  };
  if (publicMusicName) {
    inputProps.musicSrc = publicMusicName;
    inputProps.musicVolume = musicVolume;
  }

  // Write input props to a temp JSON file
  const propsPath = path.join(PROJECT_ROOT, "input-props.json");
  fs.writeFileSync(propsPath, JSON.stringify(inputProps, null, 2));

  // Calculate total duration from captions
  const lastCaption = captions[captions.length - 1];
  const totalDurationMs = Math.max(lastCaption.endMs + 2000, 10000);
  const totalFrames = Math.ceil((totalDurationMs / 1000) * FPS);

  try {
    // Use npx remotion render
    const cmd = `npx remotion render VideoComposition "${outputPath}" --props="${propsPath}" --frames=0-${totalFrames} --overwrite`;
    console.log(`  Running: ${cmd}`);
    execSync(cmd, {
      cwd: PROJECT_ROOT,
      stdio: "inherit",
      timeout: 600000, // 10 min timeout for rendering
    });
    console.log(`  ✅ Rendered to: ${outputPath}`);
    return true;
  } catch (e) {
    console.error("  ❌ Render failed:", e.message);
    return false;
  } finally {
    // Clean up
    try { fs.unlinkSync(propsPath); } catch (e) {}
  }
}

// ── Main Pipeline ────────────────────────────────────────────

async function main() {
  const args = parseArgs();
  const videoPath = args.video || args.v;
  const transcriptPath = args.transcript || args.t;

  if (!videoPath) {
    console.error("Usage: node scripts/run-pipeline.mjs --video <path> [--transcript <path>]");
    process.exit(1);
  }

  if (!fs.existsSync(videoPath)) {
    console.error(`Video not found: ${videoPath}`);
    process.exit(1);
  }

  const videoName = path.basename(videoPath, path.extname(videoPath));
  const transcriptText = transcriptPath && fs.existsSync(transcriptPath)
    ? fs.readFileSync(transcriptPath, "utf-8")
    : videoName; // fallback

  console.log("╔═══════════════════════════════════════╗");
  console.log("║  Video Automation Pipeline            ║");
  console.log("╚═══════════════════════════════════════╝");
  console.log(`Video:      ${videoPath}`);
  console.log(`Transcript: ${transcriptPath || "(auto-generated)"}`);
  console.log("");

  // Step 0: Create and clean directories
  fs.mkdirSync(B_ROLL_DIR, { recursive: true });
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const publicDir = path.join(PROJECT_ROOT, "public");
  fs.mkdirSync(publicDir, { recursive: true });
  // Clean public/ for fresh files
  for (const file of fs.readdirSync(publicDir)) {
    fs.unlinkSync(path.join(publicDir, file));
  }

  // Step 1: Estimate caption timings
  console.log("📝 Step 1: Generating timed captions...");
  const videoDuration = getVideoDuration(videoPath);
  const { captions, durationMs } = estimateCaptions(transcriptText, videoDuration);
  console.log(`  ${captions.length} captions generated over ${Math.round(durationMs / 1000)}s`);

  // Generate SRT file
  const srtContent = generateSRT(captions);
  const srtPath = path.join(OUTPUT_DIR, `${videoName}_captions.srt`);
  fs.writeFileSync(srtPath, srtContent);
  console.log(`  SRT saved: ${srtPath}`);

  // Step 2: Extract keywords
  console.log("🔑 Step 2: Extracting keywords for b-roll...");
  const keywords = extractKeywords(transcriptText);
  console.log(`  Keywords: ${keywords.join(", ")}`);

  // Step 3: Search Pixabay
  console.log("🖼️ Step 3: Searching Pixabay for b-roll clips...");
  const searchResults = await searchPixabayVideos(keywords);
  console.log(`  Found ${searchResults.length} clips`);

  // Step 4: Download b-roll
  console.log("📥 Step 4: Downloading b-roll clips...");
  const bRollFiles = searchResults.length > 0 ? await downloadBRoll(searchResults) : [];
  console.log(`  Downloaded ${bRollFiles.length} clips`);

  // Step 5: Search and download background music
  console.log("🎵 Step 5: Finding background music...");
  const musicTrack = await searchPixabayMusic("ambient inspirational");
  if (musicTrack) {
    console.log(`  Selected: "${musicTrack.title}"`);
  } else {
    console.log("  No background music found, proceeding without it");
  }

  // Step 6: Render
  console.log("🎬 Step 6: Rendering final video...");
  const outputPath = path.join(OUTPUT_DIR, `${videoName}_FINAL.mp4`);
  const success = await renderVideo(videoPath, captions, bRollFiles, outputPath, musicTrack);

  console.log("");
  console.log("╔═══════════════════════════════════════╗");
  if (success) {
    console.log("║  ✅ Pipeline Complete!                ║");
    console.log(`║  Output: ${path.basename(outputPath)}`);
  } else {
    console.log("║  ❌ Pipeline Failed                    ║");
  }
  console.log("╚═══════════════════════════════════════╝");
}

main().catch((err) => {
  console.error("Pipeline error:", err);
  process.exit(1);
});
