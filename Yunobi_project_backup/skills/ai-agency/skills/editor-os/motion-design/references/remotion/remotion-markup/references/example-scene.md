# A worked example scene

```tsx
import {
  AbsoluteFill,
  Easing,
  Interactive,
  interpolate,
  useCurrentFrame,
  useVideoConfig
} from "remotion";

export const Empty = () => {
  const {fps} = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      name="Scene"
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'white'
      }}
    >
      <Interactive.Div
        name="Title"
        style={{
          opacity: interpolate(frame, [1 * fps, 2 * fps], [0, 1], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
          fontSize: 88
        }}
      >
        Title
      </Interactive.Div>
      <Interactive.Div
        name="Subtitle"
        style={{
          opacity: interpolate(frame, [2 * fps, 3 * fps, 8 * fps, 10 * fps], [0, 1, 1, 0], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
            easing: [Easing.bezier(0.16, 1, 0.3, 1), Easing.linear, Easing.bezier(0.16, 1, 0.3, 1)],
          }),
          fontSize: 32
        }}
      >
        Subtitle
      </Interactive.Div>
    </AbsoluteFill>
  );
}
```
