import React from "react";
import { Composition } from "remotion";
import {
  CesiumFlythrough,
  type CesiumFlythroughProps,
} from "#ai-doc/skills/video/graphics/remotion/remotion-maps/techniques/cesium/assets/CesiumFlythrough";
import cityPath from "#ai-doc/skills/video/graphics/remotion/remotion-maps/techniques/cesium/assets/city-path.json";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="LandscapeFlyover"
      component={CesiumFlythrough}
      defaultProps={{ mode: "landscape" } satisfies CesiumFlythroughProps}
      durationInFrames={24 * 30}
      fps={30}
      width={1920}
      height={1080}
    />
    <Composition
      id="CityFlyover"
      component={CesiumFlythrough}
      defaultProps={
        {
          mode: "city",
          path: cityPath as [number, number][],
          altitudeStart: 700,
          altitudeEnd: 500,
          lookAheadKm: 0.7,
          travelKm: 4.5,
          pitchFromNadir: 72,
          verticalExaggeration: 1,
          maximumScreenSpaceError: 6,
        } satisfies CesiumFlythroughProps
      }
      durationInFrames={18 * 30}
      fps={30}
      width={1920}
      height={1080}
    />
  </>
);
