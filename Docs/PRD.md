# PRD: Real-Time Video-to-Sign-Language Chrome Extension

**Version:** 1.0  
**Status:** Initial specification â€” implementation not yet verified  
**Project type:** Student project / accessibility technology  
**Primary platform:** Google Chrome, Manifest V3  
**Cost constraint:** Zero-cost development using verified free and open-source resources  
**Development environment:** Antigravity, Git, local development tools

---

## 1. Product Overview

### 1.1 Product Name

Working title: **SignBridge â€” Real-Time Video-to-Sign-Language Interpreter**

The name may be changed later.

### 1.2 Problem Statement

Deaf and hard-of-hearing viewers may face accessibility barriers when watching online videos whose spoken content is not available in a sign language they understand.

Existing captions provide text, but they do not replace sign-language interpretation. A useful solution should translate video speech into sign-language animations that remain visible alongside the original video.

### 1.3 Product Vision

Build a Chrome extension that captures audio from a playing browser tab, converts speech into text, interprets that text into a selected sign language, and displays a synchronized 3D signing avatar in an unobtrusive overlay.

The initial platform is YouTube. The architecture should allow other video platforms to be added later.

The product must prioritize linguistic accuracy, accessible presentation, privacy, low latency, and zero-cost local development.

### 1.4 Product Principles

1. Accessibility and linguistic quality take priority over visual novelty.
2. ISL and ASL must be treated as distinct languages, not interchangeable sets of gestures.
3. No paid API or subscription may be required for the core local prototype.
4. No third-party asset may be used without documented usage rights.
5. The extension must not interfere with ordinary video playback.
6. Every milestone must be implemented, tested, and documented before the next major phase begins.
7. Antigravity must inspect the actual repository before modifying code.

---

## 2. Goals and Non-Goals

### 2.1 Primary Goals

- Capture audio directly from the active YouTube tab.
- Work with headphones connected or disconnected.
- Preserve normal audio playback while capture is active.
- Transcribe speech using a locally runnable speech-recognition model.
- Convert transcribed speech into a language-specific representation.
- Display a 3D avatar in a bottom-right video overlay.
- Synchronize avatar playback with speech timing and video controls.
- Provide separate ISL and ASL modes through independent language modules.
- Develop and test the core functionality without paid cloud services.
- Maintain a documented inventory of dependencies, models, datasets, and licenses.

### 2.2 Non-Goals for the Initial MVP

The initial MVP will not promise:

- Perfect or certified sign-language interpretation.
- Complete conversational vocabulary coverage.
- Support for every website or video platform.
- Automatic translation of every speaker, accent, idiom, or technical term.
- Full offline operation before all required models and assets have been downloaded.
- Production-grade accessibility certification.
- Cloud deployment, user accounts, analytics, or commercial distribution.

These may be considered later after the core workflow is validated.

---

## 3. Target Users

### Primary users

- Deaf and hard-of-hearing viewers who use ISL or ASL.
- Viewers who need sign-language support while watching online educational content.
- Accessibility researchers and student developers evaluating video interpretation technology.

### Secondary users

- Educators producing accessible learning material.
- Developers working on sign-language translation and avatar animation.
- Accessibility evaluators who can assess the quality of generated signing.

Deaf and fluent sign-language users should participate in evaluation wherever possible. Automated metrics alone are insufficient to validate linguistic quality.

---

## 4. User Stories

1. As a viewer, I want to enable the extension on YouTube so that I can see a signing avatar without leaving the video.
2. As a viewer, I want tab audio to be captured without relying on a microphone, including when I use headphones.
3. As a viewer, I want the original audio to continue playing normally.
4. As a viewer, I want to choose ISL or ASL.
5. As a viewer, I want the avatar to begin signing as speech is interpreted rather than after the entire video finishes.
6. As a viewer, I want the avatar to pause when the video pauses and recover when I seek or resume.
7. As a viewer, I want the avatar to remain unobtrusive and be repositionable or dismissible.
8. As a viewer, I want unclear or unsupported phrases to be handled honestly rather than translated into misleading gestures.
9. As a developer, I want to run the entire core workflow locally without paid API credentials.
10. As a maintainer, I want every dependency and asset to have documented license and provenance information.

---

## 5. Functional Requirements

### FR-01: Extension Initialization

- Use Chrome Manifest V3.
- Provide an extension action to start and stop interpretation.
- Require an explicit user action before starting tab audio capture.
- Display capture and processing status clearly.
- Handle unsupported pages and permission failures gracefully.

**Acceptance criteria:** The unpacked extension loads in Chrome, and the user can start and stop the feature deliberately.

### FR-02: Tab Audio Capture

- Use `chrome.tabCapture` for active-tab audio.
- Use a service worker and offscreen document where appropriate.
- Route the captured audio back to the audio output.
- Do not depend on microphone input.
- Handle capture errors, stream termination, tab closure, and navigation.
- Stop audio processing and release resources when interpretation ends.

**Acceptance criteria:** On a supported test machine, the system captures the active tab's audio with headphones both connected and disconnected, while ordinary playback remains audible.

### FR-03: Audio Segmentation

- Process audio in bounded chunks.
- Use timestamps for each audio segment.
- Support overlapping windows or another suitable strategy to avoid cutting off words at chunk boundaries.
- Manage buffering and avoid unlimited memory growth.
- Detect silence where practical.

### FR-04: Speech Recognition

- Use a locally runnable, appropriately licensed model.
- Evaluate OpenAI Whisper or a compatible local implementation.
- Do not require a hosted transcription API.
- Separate provisional transcription results from finalized segments.
- Support retry or recovery when a segment cannot be processed.
- Record processing time for evaluation without storing raw audio unnecessarily.

**Acceptance criteria:** A test video produces timestamped text segments that can be passed to the translation layer.

### FR-05: Sign-Language Translation

- Define a common interface for language-specific translators.
- Implement ISL and ASL as separate modules.
- Use language-appropriate grammar and word ordering.
- Support punctuation, numbers, common phrases, fingerspelling, and unknown terms where verified assets exist.
- Do not treat English word order or direct word substitution as sufficient sign-language translation.
- Return structured output containing sign or gloss identifiers, timing information, and any supported non-manual cues.
- Represent unsupported expressions explicitly.

**Acceptance criteria:** Each language module accepts a transcript and returns a valid, testable sequence in its defined output schema.

### FR-06: Animation and Avatar

- Use a browser-compatible 3D rendering approach, such as Three.js with React Three Fiber if appropriate.
- Render only legally usable avatar assets and animations.
- Support a defined sequence of sign animations.
- Preserve transitions between consecutive signs.
- Support facial expressions, body posture, and non-manual markers when the available animation assets permit.
- Handle missing animations gracefully.
- Avoid presenting fingerspelling as a substitute for full linguistic translation.

**Acceptance criteria:** A verified test sequence renders without broken assets or animation crashes.

### FR-07: Overlay Interface

- Display the avatar in the bottom-right corner by default.
- Keep the original video visible and usable.
- Provide controls for start/stop, language selection, visibility, and status.
- Allow repositioning or resizing where practical.
- Avoid blocking important video controls.
- Ensure the overlay is usable at common desktop resolutions.

### FR-08: Playback Synchronization

Handle the following events:

- Video play.
- Video pause.
- Video seeking.
- Video playback rate changes.
- Video ended.
- Tab navigation or closure.
- Audio capture interruption.
- Late or revised transcription segments.

The system must use timestamped segments and an explicit queue or scheduling mechanism.

It must define what happens when transcription is late. It must not silently accumulate an ever-growing queue of stale signing animations.

### FR-09: Privacy

- Process audio locally by default.
- Do not upload raw audio or transcripts to an external service without an explicit, documented decision and appropriate user notice.
- Do not persist recordings by default.
- Do not collect unnecessary browsing history, video identifiers, or personal information.
- Document model downloads and any network activity.
- Provide a visible indication when capture is active.

### FR-10: Error Handling

Provide understandable states for:

- Unsupported website.
- Audio capture denied or unavailable.
- Model unavailable.
- Transcription failure.
- Unsupported sign or missing animation.
- Backend unavailable, if a local backend is used.
- Insufficient system resources.

---

## 6. Technical Architecture

The implementation should be modular and should not depend entirely on a single external repository.

### Layer 1: Chrome Extension

Responsibilities:

- Manifest and permissions.
- Service worker.
- User controls.
- YouTube content script.
- Avatar overlay.
- Communication with the local processing service, if one is needed.

### Layer 2: Audio Capture

Responsibilities:

- Obtain a tab audio stream following explicit user interaction.
- Process the stream in an offscreen document.
- Preserve audible playback.
- Segment or forward audio for transcription.
- Manage capture lifecycle and cleanup.

### Layer 3: Speech Recognition

Responsibilities:

- Consume audio chunks.
- Generate timestamped speech segments.
- Track provisional and finalized text.
- Expose a stable interface to the translation module.

### Layer 4: Translation

Suggested interface:

`translate(transcript, targetLanguage) -> SignSequence`

The implementation should validate the output against a documented schema.

ISL and ASL must use separate translation logic, linguistic resources, and sign mappings. Shared infrastructure may be reused where appropriate.

### Layer 5: Sign Asset Registry

Responsibilities:

- Map validated sign identifiers to animation assets.
- Track source, license, attribution, and verification status.
- Mark unsupported or unverified signs.
- Prevent unapproved assets from entering the release build.

### Layer 6: Avatar Renderer

Responsibilities:

- Load permitted models and animation clips.
- Play structured sign sequences.
- Coordinate transitions and timing.
- Handle animation errors without crashing the extension.

### Layer 7: Synchronization Controller

Responsibilities:

- Coordinate transcript timestamps, animation queues, and video events.
- Discard stale queued work when necessary.
- Recover from pause, seek, playback-rate changes, and capture restarts.

---

## 7. Free-Only Technology Policy

The core development and local demonstration must not require paid services.

### Approved candidates, subject to version and dependency checks

- Chrome Manifest V3 and Chrome extension APIs.
- JavaScript or TypeScript.
- React, if needed for the overlay.
- Three.js and React Three Fiber, subject to their applicable licenses.
- Python and a local processing backend, if needed.
- OpenAI Whisper running locally, under its MIT license.
- Locally installed testing and development tools.
- Git and GitHub for source control, using their available free functionality.

### Conditional candidates

- Kozha: audit code, bundled avatar, datasets, and individual licenses separately.
- Yap Render: inspect the repository's actual license and all bundled assets before reuse.
- GenASL: inspect the repository license, pretrained models, datasets, and animation assets before reuse.
- Any ISL or ASL dataset: use only after confirming redistribution, adaptation, and intended-use permissions.
- Any hosted inference service: exclude from the required architecture unless a zero-cost, sufficiently reliable option is independently verified and explicitly approved.

### License requirements

Maintain `docs/ASSET_LICENSES.md` containing:

- Asset or dependency name.
- Source URL.
- Exact version or commit.
- License identifier and license URL.
- Required attribution.
- Whether modification is permitted.
- Whether redistribution is permitted.
- Whether commercial use is permitted.
- Restrictions and approval status.

Do not copy assets with unclear or missing licenses into the project. A repository's top-level license does not automatically cover all bundled data or third-party assets.

---

## 8. Non-Functional Requirements

### Performance

Initial engineering targets for evaluation, not guaranteed outcomes:

- Aim for a median of no more than 3 seconds from the end of a finalized speech segment to the beginning of its corresponding animation.
- Measure end-to-end latency separately from transcription latency.
- Prevent sustained growth of the pending animation queue during continuous playback.
- Keep the overlay responsive while processing audio.
- Establish a documented test-machine baseline before interpreting performance results.

### Reliability

- Capture failures must not leave playback muted.
- The extension must recover gracefully from interrupted streams.
- Unsupported signs must not crash the renderer.
- The system must release audio, model, and animation resources when stopped.

### Accessibility

- Provide visible and understandable controls.
- Maintain adequate contrast and readable status text.
- Do not rely exclusively on color to communicate errors.
- Keep the overlay unobtrusive.
- Validate signing quality with qualified or fluent sign-language users where possible.

### Maintainability

- Keep capture, transcription, translation, rendering, and synchronization independently testable.
- Define typed interfaces or equivalent schema validation.
- Avoid unnecessary dependencies.
- Document configuration and setup.
- Add tests for each new feature before integrating it into the complete pipeline.

---

## 9. Milestones and Definition of Done

### M0: Repository and License Audit

Tasks:
- Clone the candidate repositories.
- Inspect the real directory structure and dependencies.
- Run the most promising candidate locally.
- Record baseline behavior and known failures.
- Create the license inventory.

Exit criteria:
- A documented repository decision exists.
- The selected starting point has a known, reproducible setup.
- No unapproved third-party asset is required for the initial implementation.

### M1: Extension and Audio Capture

Tasks:
- Implement or adapt Manifest V3 controls.
- Implement capture initiation and offscreen audio processing.
- Preserve audible playback.
- Handle stopping, navigation, and capture errors.

Exit criteria:
- The audio-capture test suite passes.
- Playback remains audible with and without headphones.
- Lifecycle cleanup is verified.

### M2: Local Transcription

Tasks:
- Integrate local speech recognition.
- Implement audio segmentation.
- Produce timestamped transcript segments.
- Measure latency and resource use.

Exit criteria:
- A repeatable test video generates transcript segments.
- Failures and missing segments are reported.
- No paid API is required.

### M3: First Language End-to-End Prototype

Tasks:
- Select the first language based on verified asset availability and achievable scope.
- Implement the language-specific translator.
- Define the sign-sequence schema.
- Integrate a small, verified animation vocabulary.

Exit criteria:
- A supported video segment can be captured, transcribed, translated, and rendered automatically.
- Unsupported vocabulary is reported honestly.
- The end-to-end workflow is repeatable.

### M4: Synchronization and Usability

Tasks:
- Implement pause, resume, seeking, and queue-reset behavior.
- Refine the overlay.
- Test longer videos and repeated playback.

Exit criteria:
- No major synchronization failures occur in the defined test suite.
- The extension can stop and restart without requiring a browser restart.

### M5: Second Language

Tasks:
- Add the second language as an independent module.
- Validate language-specific output.
- Reuse shared capture and rendering infrastructure where suitable.

Exit criteria:
- Both language modes pass their own tests.
- Their coverage and limitations are documented separately.

### M6: Evaluation and Release Preparation

Tasks:
- Evaluate with fluent sign-language users.
- Measure latency and translation coverage.
- Verify dependency and asset licenses.
- Document installation, known limitations, and privacy behavior.

Exit criteria:
- A reproducible demonstration exists.
- The test report and license inventory are complete.
- No unapproved asset or paid service is required by the core prototype.

---

## 10. Testing Strategy

### Unit tests

- Audio chunk boundaries.
- Transcript timestamp validation.
- Translation schema validation.
- Sign identifier resolution.
- Animation queue management.
- Playback-state transitions.
- License registry validation.

### Integration tests

- Capture audio and preserve playback.
- Pass audio chunks into local transcription.
- Pass transcript segments into the translation module.
- Render supported signs.
- Recover from missing assets and processing errors.

### End-to-end tests

Use a small, legally usable set of test videos or original recordings with known transcripts.

Test:
- Clear speech.
- Short pauses.
- Continuous speech.
- Unsupported vocabulary.
- Video pause and resume.
- Seeking backward and forward.
- Headphones connected and disconnected.
- Stopping capture and restarting it.

### Evaluation metrics

Report:
- Word error rate or another suitable transcription metric.
- Sign coverage on the test vocabulary.
- Human-rated linguistic accuracy.
- Median and 95th-percentile latency.
- Synchronization failures.
- Animation failures.
- CPU and memory usage.
- Results separately for ISL and ASL.

Do not claim high translation accuracy without an appropriate evaluation dataset and human review.

---

## 11. Antigravity Development Workflow

The PRD is the source of truth. Antigravity must implement the project incrementally rather than attempting a complete rewrite in one instruction.

### Required documentation

Create and maintain:

- `docs/PRD.md` â€” this product specification.
- `docs/ARCHITECTURE.md` â€” current architecture and data flow.
- `docs/IMPLEMENTATION_PLAN.md` â€” milestones and task status.
- `docs/ASSET_LICENSES.md` â€” dependency and asset license inventory.
- `docs/TEST_PLAN.md` â€” test cases and acceptance criteria.
- `docs/DECISIONS.md` â€” architectural decisions and their rationale.
- `README.md` â€” setup, execution, testing, and troubleshooting.

### Implementation rules

1. Inspect the existing repository before changing anything.
2. Report the current state and identify discrepancies with the PRD.
3. Propose a minimal implementation plan for the current milestone.
4. Do not modify unrelated components.
5. Do not add paid APIs or unverified third-party assets.
6. Implement one milestone at a time.
7. Run relevant tests and report their actual results.
8. Update documentation and the task checklist after each milestone.
9. Do not mark a feature complete if it has only been written but not tested.
10. Request human approval before major architectural changes or adding a dependency with unclear licensing.
11. Never expose API keys, credentials, or private user data in source code or logs.
12. Keep the implementation reproducible on a clean local development environment.

---

## 12. Risks and Mitigations

**Risk: Incomplete ISL or ASL animation vocabulary.**  
Mitigation: Start with a deliberately small, verified vocabulary and report unsupported phrases.

**Risk: Repository licensing conflicts.**  
Mitigation: Maintain an asset-level license inventory and exclude unverified assets.

**Risk: Local transcription latency.**  
Mitigation: Benchmark on the actual development machine, evaluate model sizes, and tune audio chunking before considering more complex infrastructure.

**Risk: Translation quality is inadequate.**  
Mitigation: Separate linguistic translation from animation, test with fluent users, and avoid claiming full interpretation prematurely.

**Risk: Captured audio is no longer audible.**  
Mitigation: Make audio routing and cleanup explicit and test them before AI integration.

**Risk: Animation becomes unsynchronized.**  
Mitigation: Use timestamps, a bounded queue, and explicit playback-state handling.

**Risk: Scope becomes too large.**  
Mitigation: Finish one end-to-end language pipeline before implementing the second.

**Risk: Hidden runtime costs.**  
Mitigation: Require local inference and local execution for the core MVP. Document optional costs separately.

---

## 13. Final Acceptance Criteria

The MVP is considered complete only when:

- The extension loads in Chrome.
- The user can explicitly start and stop interpretation.
- Active-tab audio is captured without microphone dependence.
- Ordinary audio playback is preserved.
- Local speech recognition produces timestamped transcript segments.
- At least one language-specific translation pipeline produces structured signing output.
- The avatar renders supported animations in the overlay.
- Pause, resume, seek, and stop behavior are tested.
- The complete workflow runs without mandatory paid APIs.
- Every shipped third-party dependency and asset has an approved license record.
- Setup instructions, tests, measured results, and limitations are documented.

Support for the second language is a separate milestone and must be validated independently.

---

## 14. Immediate Next Action

Do not begin by implementing every component.

Start with **M0: Repository and License Audit**. Inspect Kozha, Yap Render, GenASL, and SignZen, identify which components can legally be reused, run the most promising baseline, and recommend a final implementation strategy.

After the audit, update the architecture and implementation plan before starting M1.

The project is successful when it delivers a reproducible, zero-cost local prototype with demonstrable sign-language outputâ€”not merely when the extension UI or avatar looks complete.
