import React, { useMemo } from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { VideoCompositionProps, Caption } from "./types";

// ── Caption overlay ──────────────────────────────────────────
const CaptionOverlay: React.FC<{ captions: Caption[] }> = ({ captions }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentMs = (frame / fps) * 1000;

  // Find the caption active at this moment
  const active = useMemo(() => {
    return captions.find((c) => currentMs >= c.startMs && currentMs <= c.endMs);
  }, [captions, currentMs]);

  if (!active) return null;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: 80,
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(0, 0, 0, 0.65)",
          backdropFilter: "blur(4px)",
          borderRadius: 12,
          padding: "14px 28px",
          margin: "0 40px",
          maxWidth: "90%",
        }}
      >
        <span
          style={{
            color: "white",
            fontSize: 36,
            fontFamily: "system-ui, -apple-system, sans-serif",
            fontWeight: 600,
            lineHeight: 1.4,
            textAlign: "center",
            display: "block",
          }}
        >
          {active.text}
        </span>
      </div>
    </AbsoluteFill>
  );
};

// ── B-roll overlay (picture-in-picture) ──────────────────────
const BRollOverlay: React.FC<{ clips: NonNullable<VideoCompositionProps["bRollClips"]> }> = ({
  clips,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const currentMs = (frame / fps) * 1000;

  const activeClip = useMemo(() => {
    return clips.find(
      (c) => currentMs >= c.startMs && currentMs <= c.startMs + c.durationMs
    );
  }, [clips, currentMs]);

  if (!activeClip) return null;

  // Fade in/out
  const clipProgress = (currentMs - activeClip.startMs) / activeClip.durationMs;
  const opacity = clipProgress < 0.05
    ? clipProgress / 0.05
    : clipProgress > 0.95
      ? (1 - clipProgress) / 0.05
      : 1;

  return (
    <AbsoluteFill
      style={{
        justifyContent: "flex-end",
        alignItems: "flex-end",
        padding: 40,
      }}
    >
      <div
        style={{
          width: "35%",
          height: "auto",
          borderRadius: 16,
          overflow: "hidden",
          border: "3px solid white",
          boxShadow: "0 4px 24px rgba(0,0,0,0.3)",
          opacity: Math.max(0, Math.min(1, opacity)),
        }}
      >
        <OffthreadVideo
          src={staticFile(activeClip.src)}
          style={{ width: "100%", height: "100%" }}
        />
      </div>
    </AbsoluteFill>
  );
};

// ── Main Composition ─────────────────────────────────────────
export const VideoComposition: React.FC<VideoCompositionProps> = ({
  mainVideoSrc,
  captions,
  bRollClips = [],
  musicSrc,
  musicVolume = 0.15,
}) => {
  const { fps } = useVideoConfig();

  // Calculate the main video duration in frames
  const mainDuration = useMemo(() => {
    if (captions.length === 0) return fps * 45; // fallback
    const last = captions[captions.length - 1];
    return Math.ceil((last.endMs / 1000) * fps) + fps; // +1 sec padding
  }, [captions, fps]);

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {/* Main talking head video */}
      {mainVideoSrc && (
        <Sequence from={0} durationInFrames={mainDuration}>
          <OffthreadVideo
            src={staticFile(mainVideoSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        </Sequence>
      )}

      {/* Background music (audio only, low volume behind speech) */}
      {musicSrc && (
        <Sequence from={0} durationInFrames={mainDuration}>
          <Audio
            src={staticFile(musicSrc)}
            volume={musicVolume}
            loop
          />
        </Sequence>
      )}

      {/* B-roll picture-in-picture */}
      {bRollClips.length > 0 && (
        <Sequence from={0} durationInFrames={mainDuration}>
          <BRollOverlay clips={bRollClips} />
        </Sequence>
      )}

      {/* Caption overlay */}
      {captions.length > 0 && (
        <Sequence from={0} durationInFrames={mainDuration}>
          <CaptionOverlay captions={captions} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
