export interface Caption {
  startMs: number;
  endMs: number;
  text: string;
}

export interface BRollClip {
  src: string;
  startMs: number;
  durationMs: number;
}

export interface VideoCompositionProps {
  // These should be filenames relative to public/ (e.g., "input.mp4", "broll_0.mp4")
  mainVideoSrc: string;
  captions: Caption[];
  bRollClips?: BRollClip[];
  musicSrc?: string;
  musicVolume?: number; // 0.0 to 1.0
}
