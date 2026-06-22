/**
 * Unified TTS Abstraction Layer
 * Supports both offline (Supertonic, Kokoro) and online (Edge TTS) providers
 * Can be used in video-automation pipeline or standalone
 */

import { spawn } from "child_process";
import { writeFileSync, existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export type TTSProvider = "supertonic" | "kokoro" | "edge" | "auto";
export type TTSVoice = "F1" | "F2" | "F3" | "F4" | "F5" | "M1" | "M2" | "M3" | "M4" | "M5" 
  | "af_sarah" | "af_alloy" | "af_bella" | "af_jessica" | "af_nicole" | "af_nova" | "af_river" | "af_sky"
  | "am_adam" | "am_echo" | "am_eric" | "am_fenrir" | "am_liam" | "am_michael" | "am_onyx" | "am_puck"
  | "bf_alice" | "bf_emma" | "bf_isabella" | "bf_lily" | "bm_daniel" | "bm_fable" | "bm_george" | "bm_lewis"
  | string;

export interface TTSOptions {
  provider?: TTSProvider;
  voice?: TTSVoice;
  speed?: number;
  outputPath?: string;
  language?: string;
}

export interface TTSResult {
  success: boolean;
  outputPath?: string;
  durationMs?: number;
  provider?: string;
  error?: string;
}

/**
 * Unified TTS class supporting multiple providers
 */
export class UnifiedTTS {
  private supertonic: any = null;
  private kokoro: any = null;
  private initialized = false;

  constructor() {}

  async initialize(): Promise<void> {
    if (this.initialized) return;
    
    // Try to load Supertonic
    try {
      const supertonic = await import("supertonic");
      this.supertonic = new supertonic.TTS();
      console.log("[TTS] Supertonic loaded:", this.supertonic.voice_style_names);
    } catch (e) {
      console.log("[TTS] Supertonic not available:", (e as Error).message);
    }

    // Try to load Kokoro
    try {
      const kokoro = await import("kokoro_onnx");
      this.kokoro = new kokoro.Kokoro(
        "C:/Users/tbank/Desktop/kokoro-v1.0.onnx",
        "C:/Users/tbank/Desktop/voices-v1.0.bin"
      );
      console.log("[TTS] Kokoro loaded");
    } catch (e) {
      console.log("[TTS] Kokoro not available:", (e as Error).message);
    }

    this.initialized = true;
  }

  /**
   * Generate speech with automatic provider selection
   */
  async speak(text: string, options: TTSOptions = {}): Promise<TTSResult> {
    await this.initialize();

    const provider = options.provider || "auto";
    const voice = options.voice || "F1";
    const speed = options.speed || 1.0;
    const language = options.language || "en-us";
    const outputPath = options.outputPath || `./tts-output-${Date.now()}.wav`;

    // Auto-select provider
    let selectedProvider: string;
    let selectedVoice: string;

    if (provider === "auto") {
      // Prefer offline providers
      if (this.supertonic) {
        selectedProvider = "supertonic";
        selectedVoice = this.mapVoice("supertonic", voice);
      } else if (this.kokoro) {
        selectedProvider = "kokoro";
        selectedVoice = this.mapVoice("kokoro", voice);
      } else {
        selectedProvider = "edge";
        selectedVoice = voice;
      }
    } else {
      selectedProvider = provider;
      selectedVoice = this.mapVoice(provider, voice);
    }

    console.log(`[TTS] Using ${selectedProvider} with voice ${selectedVoice}`);

    try {
      let result: TTSResult;

      switch (selectedProvider) {
        case "supertonic":
          result = await this.speakSupertonic(text, selectedVoice, outputPath);
          break;
        case "kokoro":
          result = await this.speakKokoro(text, selectedVoice, outputPath);
          break;
        case "edge":
          result = await this.speakEdge(text, selectedVoice, outputPath);
          break;
        default:
          throw new Error(`Unknown provider: ${selectedProvider}`);
      }

      return { ...result, provider: selectedProvider };

    } catch (error) {
      console.error(`[TTS] ${selectedProvider} failed:`, error);
      
      // Fallback to next available provider
      if (selectedProvider !== "edge" && this.kokoro) {
        console.log("[TTS] Falling back to Kokoro...");
        return this.speakKokoro(text, this.mapVoice("kokoro", voice), outputPath);
      }
      if (selectedProvider !== "edge" && this.supertonic) {
        console.log("[TTS] Falling back to Supertonic...");
        return this.speakSupertonic(text, this.mapVoice("supertonic", voice), outputPath);
      }
      
      return {
        success: false,
        error: (error as Error).message,
        provider: selectedProvider
      };
    }
  }

  private mapVoice(provider: string, voice: string): string {
    const voiceMap: Record<string, Record<string, string>> = {
      supertonic: {
        "F1": "F1", "F2": "F2", "F3": "F3", "F4": "F4", "F5": "F5",
        "M1": "M1", "M2": "M2", "M3": "M3", "M4": "M4", "M5": "M5",
        "af_sarah": "F1", "af_alloy": "F2", "af_bella": "F3",
        "am_adam": "M1", "am_echo": "M2"
      },
      kokoro: {
        "F1": "af_sarah", "F2": "af_alloy", "F3": "af_bella", "F4": "af_nova", "F5": "af_sky",
        "M1": "am_adam", "M2": "am_echo", "M3": "am_eric", "M4": "am_fenrir", "M5": "am_liam",
        "af_sarah": "af_sarah", "af_alloy": "af_alloy", "af_bella": "af_bella",
        "am_adam": "am_adam", "am_echo": "am_echo"
      },
      edge: {
        "F1": "en-US-AriaNeural", "F2": "en-US-JennyNeural",
        "M1": "en-US-GuyNeural", "M2": "en-US-DavisNeural"
      }
    };

    return voiceMap[provider]?.[voice] || voice;
  }

  private async speakSupertonic(text: string, voice: string, outputPath: string): Promise<TTSResult> {
    if (!this.supertonic) throw new Error("Supertonic not initialized");

    const style = this.supertonic.get_voice_style(voice);
    const audioTuple = this.supertonic.synthesize(text, style);
    
    // Handle tuple return: [audio, ...]
    let audio = audioTuple[0];
    if (audio.ndim > 1) audio = audio.squeeze();
    
    // Save using soundfile
    const soundfile = await import("soundfile");
    soundfile.writeSync(outputPath, audio, 44100);
    
    return { success: true, outputPath };
  }

  private async speakKokoro(text: string, voice: string, outputPath: string): Promise<TTSResult> {
    if (!this.kokoro) throw new Error("Kokoro not initialized");

    const { create } = await import("kokoro_onnx");
    const audio = this.kokoro.create(text, { voice, speed: 1.0, lang: "en-us" });
    
    const soundfile = await import("soundfile");
    soundfile.writeSync(outputPath, audio, 24000);
    
    return { success: true, outputPath };
  }

  private async speakEdge(text: string, voice: string, outputPath: string): Promise<TTSResult> {
    // Use Edge TTS via edge-tts CLI (needs: pip install edge-tts)
    return new Promise((resolve, reject) => {
      const edgeTts = spawn("edge-tts", [
        "--text", text,
        "--voice", voice,
        "--write-media", outputPath
      ]);

      let stderr = "";
      edgeTts.stderr?.on("data", (data) => stderr += data.toString());
      
      edgeTts.on("close", (code) => {
        if (code === 0) {
          resolve({ success: true, outputPath });
        } else {
          reject(new Error(`Edge TTS failed: ${stderr}`));
        }
      });
    });
  }
}

// Export singleton
export const tts = new UnifiedTTS();

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  const text = args[0] || "Hello, this is a test of the unified TTS system.";
  const voice = args[1] || "F1";
  const provider = args[2] as "supertonic" | "kokoro" | "edge" | "auto" || "auto";

  const tts = new UnifiedTTS();
  await tts.initialize();
  
  const result = await tts.speak(text, { provider: provider as any, voice });
  console.log("Result:", result);
}

export default UnifiedTTS;