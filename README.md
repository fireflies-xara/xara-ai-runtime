# XARA AI Runtime

The on-device perception engine for XARA ONE's digital signage screens. Runs on each screen's attached PC, reads a depth camera, detects and tracks visitors, estimates demographics/attention/emotion, decides what content to play, and reports audience + playback data back to the XARA ONE backend.

This is a separate Python project from `backend/` (FastAPI) and `frontend/` (Next.js) — it ships and runs independently on edge hardware, communicating with the backend only over HTTP (see `connect_backend.py` / `modules/ad_engine/backend_client.py`).

## Processing pipeline

From `xara_runtime.py`'s own header — this is the authoritative order, unchanged since the original runtime, with each stage now wrapped in a plugin:

```
Camera → RT-DETR → BoT-SORT → Distance → Zone → Face →
Face State → Head Pose → Attention → State Managers →
Event Engine → Overlay → (Backend / Dashboard)
```

- **Camera**: Intel RealSense depth camera (`camera/realsense_camera.py`, `pyrealsense2`)
- **RT-DETR**: real-time object/person detection (`ultralytics`, model weights in `rtdetr-l.pt`)
- **BoT-SORT**: multi-object tracking across frames
- **Distance / Zone**: depth-based proximity and zone-of-interest classification
- **Face / Face State / Head Pose / Attention**: `mediapipe`-based face and gaze analysis
- **Demographics**: age/gender via **MiVOLO v2** (`MiVOLO/`, `third_party/`) — replaces the original MiVOLO v1 + Swin combination; this is the one AI model swap noted in the runtime's own header, everything else in the pipeline is unchanged
- **Event Engine**: turns per-frame detections into visitor sessions (entry/exit, dwell time) and ad-decision events
- **Overlay**: on-screen debug visualization
- **Backend / Dashboard**: HTTP calls to the XARA ONE backend (device heartbeat, telemetry, ad matching, audience session submission, playback updates) — see `modules/ad_engine/backend_client.py`

Each pipeline stage lives behind a plugin wrapper in `plugins/` (`RTDETRPlugin`, `DistancePlugin`, `ZonePlugin`, `FacePlugin`, `EmotionPlugin`, `GazePlugin`, `HeadPosePlugin`, ...), so an individual stage can be swapped without touching the orchestration in `xara_runtime.py`.

There is also a separate, simpler `main.py` (`EventBus` / `StateStore` / `ModuleManager`) — a lighter-weight orchestration scaffold, distinct from `xara_runtime.py`'s plugin pipeline. If you're running the real on-device perception loop, use `xara_runtime.py`; `main.py` is a different, smaller entry point.

## Setup

```powershell
.\start.ps1
```

This script will, on first run:
1. Copy `.env.example` → `.env` if `.env` doesn't exist yet.
2. Create a `venv/` virtual environment if one isn't already present.
3. Install `requirements.txt` into it.
4. Launch `xara_runtime.py`.

On later runs it just activates the existing `venv` and launches the runtime directly.

### Configuration (`.env`)

| Variable | Purpose |
|---|---|
| `BACKEND_URL` | Base URL of the XARA ONE backend this device talks to (default `http://127.0.0.1:8000` for local development) |
| `BACKEND_AUTO_REGISTER` | `1` to auto-register this device with the backend on first run if its MAC address isn't already known (the device still needs to be assigned to a screen afterward) |
| `XARA_SCREENSAVER_PATH` | Optional, currently unused (marked "future use" in `.env.example`) |

**Device identity is resolved automatically from this machine's MAC address at startup** (`modules/runtime/device_resolver.py`) — do not hardcode a device ID in `.env`.

### Checking backend connectivity without starting the full runtime

```powershell
venv\Scripts\python.exe connect_backend.py
```

Prints this machine's resolved MAC address and whether the configured backend can find/reach it (`GET {BACKEND_URL}/devices/lookup/by-mac`) — useful for confirming device registration before running the full perception pipeline.

## Running

```powershell
venv\Scripts\python.exe xara_runtime.py
```

(`start.ps1` does this for you, including first-time environment setup.) On launch, the runtime first calls `bootstrap_runtime.relaunch_if_wrong_interpreter()` (re-execs itself under the correct Python/venv if needed) and `resolve_device_identity()` before any camera/model code runs.

## Testing

```powershell
.\run_runtime.ps1
```

Runs `tests/test_xara_runtime.py` through the project's own venv. The `tests/` directory covers each pipeline stage individually (`test_rtdetr.py`, `test_tracking.py`, `test_distance.py`, `test_zones.py`, `test_face_detection.py`, `test_face_mesh.py`, `test_emotion_live.py`, `test_mivolo_v2*.py`, `test_pose.py`, `test_attention.py`, `test_realsense.py`, `test_depth_point.py`, `test_l2cs.py`, `test_insightface_gpu.py`) plus integration-level tests (`test_ad_decision_engine.py`, `test_ai_decision_interval.py`, `test_events.py`, `test_transitions.py`, `test_visitor_manager.py`, `test_activity.py`, `test_device_resolver.py`, `test_machine_id.py`, `test_media_cache.py`, `test_model_inspector.py`, `test_speed_engine.py`, `test_camera.py`, `test_demographics.py`).

## Project layout

| Path | Contents |
|---|---|
| `xara_runtime.py` | Main entry point — the full plugin-based perception pipeline described above |
| `main.py` | Secondary, simpler entry point (`EventBus`/`StateStore`/`ModuleManager` scaffold) |
| `bootstrap_runtime.py` | Interpreter/venv re-exec guard, runs before anything else |
| `connect_backend.py` | Standalone backend-connectivity/device-identity check |
| `plugins/` | Thin wrappers adapting each `modules/` component into the `xara_runtime.py` pipeline |
| `modules/` | The actual AI/business logic per concern: `detection`, `tracking`, `depth`, `zone`, `face`, `emotion`, `gaze`, `headpose`, `attention`, `demographics`, `engagement`, `activity`, `crowd`, `gesture`, `motion`, `identity`, `pose`, `state`, `events`, `engine`, `ad_engine` (backend HTTP client + ad-decision logic), `runtime` (device resolver, config), `hardware`, `latency`, `validation`, `overlay` |
| `camera/` | RealSense depth-camera capture |
| `core/` | `EventBus`/`StateStore`/`ModuleManager` used by `main.py` |
| `api/`, `dashboard/` | Empty packages (`__init__.py` only) — scaffolded, not yet implemented |
| `events/` | Runtime config / event plumbing used by `xara_runtime.py` |
| `config/` | Configuration files |
| `MiVOLO/`, `third_party/` | Vendored third-party age/gender model code (not XARA-authored — out of scope for XARA-side code review) |
| `storage/` | Local on-device storage (media cache, etc.) |
| `scripts/` | Utility/maintenance scripts |
| `tests/` | Per-module and integration tests, see **Testing** above |
| `Log/` | Runtime log output |
| `rtdetr-l.pt` | RT-DETR detection model weights (~66MB, checked into this directory) |

## Key dependencies

Full list in `requirements.txt`. The core vision/ML stack: `torch`/`torchvision` 2.12, `ultralytics` (RT-DETR), `opencv-python`, `mediapipe`, `pyrealsense2` (Intel RealSense SDK bindings), `numpy`, `fastapi` (used for this project's own local `api/`, separate from the main backend). There's also a `requirements_clean.txt` alongside the main `requirements.txt` — if you're setting up a fresh environment and the full `requirements.txt` gives you trouble, that's the one to check first; the difference between the two wasn't audited for this document.

## Talking to the backend

This runtime is a pure HTTP client of the backend — it has no server-side route table the backend calls into. Confirmed call sites (from `modules/ad_engine/backend_client.py`, traced in `audit/06_API_DATABASE_MAPPING.md` §1 of this repository's backend architecture audit):

- Device registration/heartbeat/telemetry (on startup, and periodically — heartbeat ~every 60s, full hardware telemetry ~every 5s on a background thread)
- `POST /api/v1/ad-engine/match` — content selection per detection tick
- `GET /devices/{device_id}/active-playlist` — playlist fallback
- `GET /api/player/{screen_id}/screen-saver` — screensaver config, polled ~every 30s
- `POST /audience-sessions` — one call per visitor exit, submitting the session's detected demographics/attention/emotion data
- Playback-state updates per content switch

See `audit/06_API_DATABASE_MAPPING.md` and `audit/19_PHASE3_BACKEND_EXECUTION_FLOW.md` in the main repository for the backend-side trace of these same calls, and `security-audits/analytics-data-lineage-review/` for how the data this runtime submits (`audience_type`, `dominant_emotion`, attention scores) flows into the Analytics dashboard, including which of those fields have confirmed vs. still-open data-population questions.
