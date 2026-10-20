# Security Policy

## Supported Versions

SignBridge is currently a research prototype in active milestone development.

| Version | Supported | Status |
|---|---|---|
| `0.2.0` (M4 Stage 5) | :white_check_mark: | Active Development Baseline |
| `< 0.2.0` (M1–M3) | :x: | Superseded |

---

## Threat Model & Security Architecture

SignBridge operates under a strict **local-first** security model:
1. **Local Loopback Binding:** The Python FastAPI backend binds exclusively to `127.0.0.1:8765`. It never listens on public interfaces (`0.0.0.0`).
2. **CORS Restrictions:** Cross-Origin Resource Sharing is strictly constrained to Chrome extension origins (`chrome-extension://*`) and localhost.
3. **No Cloud Audio Transmission:** Tab audio captured via `chrome.tabCapture` is processed in memory on the local CPU and is never transmitted across the network.
4. **Least Privilege Manifest:** Chrome Manifest V3 permissions are minimal (`tabCapture`, `offscreen`, `activeTab`, `storage`, `scripting`). No physical microphone or broad `<all_urls>` permissions are requested.
5. **No File Persistence:** Audio slices exist only in RAM during transcription (2.0s duration) and are cleared immediately upon request completion.

### Known Environmental Limitations
- **Local Multi-User Environments:** Because the local loopback service (`127.0.0.1:8765`) does not implement user authentication, other local processes running under the same OS user account can communicate with the service. For pilot testing and sensitive evaluation, SignBridge must be executed on a dedicated single-user workstation.

---

## Reporting a Vulnerability

If you discover a potential security vulnerability or privacy leak within SignBridge:

1. **Do NOT open a public GitHub issue.**
2. Send a detailed report to the project maintainers via email or security advisory.
3. Include:
   - A description of the issue and potential impact.
   - Exact steps or script to reproduce the behavior locally.
   - Operating system, browser version, and Python environment.
4. **Data Sanitization:** When providing logs or diagnostic traces, ensure you **do not include**:
   - Raw audio WAV files or audio buffers.
   - Real private speech transcripts.
   - Local directory paths containing personal usernames.
   - Internal network tokens or credentials.

We will acknowledge receipt within 48 hours and work with you on a responsible remediation timeline.
