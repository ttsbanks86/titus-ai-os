const { spawn } = require("child_process");

class UnifiedTTS {
  async speak(text, options = {}) {
    const provider = options.provider || "auto";
    const voice = options.voice || "F1";
    const outputPath = options.outputPath || `./tts-output-${Date.now()}.wav`;

    let selectedProvider;
    
    if (options.provider === "auto") {
      const available = await this.checkAvailable();
      if (available.supertonic) selectedProvider = "supertonic";
      else if (available.kokoro) selectedProvider = "kokoro";
      else selectedProvider = "edge";
    } else {
      selectedProvider = options.provider;
    }

    console.log(`[TTS] Using ${selectedProvider}`);

    try {
      switch (selectedProvider) {
        case "supertonic":
          return await this.speakSupertonic(text, options.voice, options.outputPath);
        case "kokoro":
          return await this.speakKokoro(text, options.voice, options.outputPath);
        case "edge":
          return await this.speakEdge(text, options.voice, options.outputPath);
        default:
          throw new Error(`Unknown provider: ${selectedProvider}`);
      }
    } catch (error) {
      console.error(`[TTS] Failed:`, error);
      return { success: false, error: error.message };
    }
  }

  async checkAvailable() {
    return {
      supertonic: await this.checkPythonModule("supertonic"),
      kokoro: await this.checkPythonModule("kokoro_onnx"),
      edge: await this.checkCommand("edge-tts")
    };
  }

  checkPythonModule(module) {
    return new Promise((resolve) => {
      const proc = spawn("python", ["-c", `import ${module}; print("ok")`]);
      proc.on("close", (code) => resolve(code === 0));
      proc.on("error", () => resolve(false));
    });
  }

  checkCommand(cmd) {
    return new Promise((resolve) => {
      const proc = spawn("where", [cmd]);
      proc.on("close", (code) => resolve(code === 0));
      proc.on("error", () => resolve(false));
    });
  }

  speakSupertonic(text, voice, outputPath) {
    return new Promise((resolve, reject) => {
      const script = `
import supertonic
import soundfile as sf

tts = supertonic.TTS()
style = tts.get_voice_style("${voice}")
audio = tts.synthesize("${text.replace(/"/g, '\\"')}", style)
audio = audio[0].squeeze()
import soundfile as sf
sf.write(r"${outputPath.replace(/\\/g, '\\\\')}", audio, 44100)
print("OK")
`;
      
      const proc = spawn("python", ["-c", script]);
      let stdout = "", stderr = "";
      proc.stdout?.on("data", d => stdout += d);
      proc.stderr?.on("data", d => console.error("[Supertonic]", d.toString()));
      
      proc.on("close", (code) => {
        if (code === 0) {
          resolve({ success: true, outputPath, provider: "supertonic" });
        } else {
          reject(new Error("Supertonic failed"));
        }
      });
    });
  }

  speakKokoro(text, voice, outputPath) {
    return new Promise((resolve, reject) => {
      const script = `
import kokoro_onnx
import soundfile as sf
import numpy as np

model = kokoro_onnx.Kokoro(
    "C:/Users/tbank/Desktop/Live Cowork/video-automation/models/kokoro-v1.0.onnx",
    "C:/Users/tbank/Desktop/Live Cowork/video-automation/models/voices-v1.0.bin"
)
audio, sample_rate = model.create(
    """${text.replace(/"/g, '\\"')}""", 
    voice="${voice}", 
    speed=1.0, 
    lang="en-us"
)
if audio.ndim > 1:
    audio = audio.squeeze()
audio = audio.astype(np.float32)
import soundfile as sf
sf.write(r"${outputPath.replace(/\\/g, '\\\\')}", audio, sample_rate)
print("OK")
`;
      
      const proc = spawn("python", ["-c", script]);
      let stdout = "", stderr = "";
      proc.stdout?.on("data", d => stdout += d);
      proc.stderr?.on("data", d => console.error("[Kokoro]", d.toString()));
      
      proc.on("close", (code) => {
        if (code === 0) {
          resolve({ success: true, outputPath, provider: "kokoro" });
        } else {
          reject(new Error("Kokoro failed"));
        }
      });
    });
  }

  speakEdge(text, voice, outputPath) {
    return new Promise((resolve, reject) => {
      const proc = spawn("edge-tts", [
        "--text", text,
        "--voice", voice,
        "--write-media", outputPath
      ]);

      let stderr = "";
      proc.stderr?.on("data", (data) => stderr += data.toString());
      
      proc.on("close", (code) => {
        if (code === 0) {
          resolve({ success: true, outputPath, provider: "edge" });
        } else {
          reject(new Error("Edge TTS failed"));
        }
      });
    });
  }
}

module.exports = { UnifiedTTS };