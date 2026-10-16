---
paths:
  - "**/*.swift"
  - "**/project.yml"
  - "**/Makefile"
---
<!-- vibekit:rule -->
<!-- Generated. Edited in the source this repo is projected from, never here. -->

# Swift

- **Never call `xcodebuild` or `xcodegen` raw.** It re-resolves the shared package graph under a running Xcode.app, and the error names the wrong thing. Use `make build`, `make test`, `make verify`, `make generate`. When a build fails, rerun with `XCBEAUTIFY=cat` or the real `file.swift:12:5: error:` lines are gone.
- **A concurrency error usually means the ownership is wrong**, not that an annotation is missing. Never silence one with `nonisolated(unsafe)` or a detached task you can't explain.
- **Extensions have budgets.** A keyboard extension dies around 60MB, and share and widget extensions are tighter. Check which target an import lands in before you add it.
- **Tests are Swift Testing** (`@Suite`, `@Test`, `#expect`), never XCTest, except XCUITest for E2E.
- **Log through the project's subsystem helper** (Wavenote: `LogSubsystem.logger(_:)`), never `print`.
- **`// MARK: -` for sections.** Comments say why, and the best one names the alternative you rejected.
- **User-facing strings are localizable, never name a part of the machine, and keep every sentence to 12 words, two sentences a string.** Ramzi, 30 Sep 2026, on a paywall paragraph: "way too verbose". cutkit's `ios/Scripts/lint-copy.mjs` enforces it; copy it into any app that lacks one.
- **Segmented pickers and tab bars get `.controlSize(.large)`**, so they match iOS 27 and the tap target clears 44pt. The default is a squat strip, and Ramzi has had to flag it more than once (29 Sep 2026).
- **A nested `enum Color` or `enum Font` shadows SwiftUI's**, so `Color(red:)` inside it stops compiling. Write `SwiftUI.Color` in generated token files, and typecheck them with `xcrun swiftc -typecheck` before calling them done.
- **A capture writer input keeps `expectsMediaDataInRealTime = true`**, deprecation warning and all. iOS 27's `appendImmediately` doesn't imply it, so without it cutkit's recorder threw away 2 of every 3 frames (30 Sep 2026).
- **Retiming a `CMSampleBuffer` sizes its array by timing entries, not samples.** Ask `CMSampleBufferGetSampleTimingInfoArray` for the count first. An audio buffer holds about 1024 samples under one entry, and a per-sample array made cutkit's resumed takes silent (1 Oct 2026).
- **Ported code isn't yours to tidy.** Where a project says a file came from a sibling repo, leave its shape alone, or the next port becomes a merge conflict for nothing.

Depth: the `swift` skill.
