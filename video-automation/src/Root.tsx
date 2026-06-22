import React from "react";
import { Composition } from "remotion";
import { VideoComposition } from "./VideoComposition";
import type { VideoCompositionProps } from "./types";

// 200 seconds at 30fps — max duration; actual render length is controlled
// by the --frames flag passed from the pipeline.
const FPS = 30;
const MAX_DURATION = 200 * FPS; // 6000 frames

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VideoComposition"
        component={VideoComposition}
        durationInFrames={MAX_DURATION}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={
          {
            mainVideoSrc: "",
            captions: [],
            bRollClips: [],
          } as VideoCompositionProps
        }
      />
    </>
  );
};
