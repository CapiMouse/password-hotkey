# CLAUDE.md — Developer Guide for Claude Code

> ⚠️ This file is a **technical guide** for Claude Code agents working on this project.
> It is not a feature, not a module, and not executable code.
> Its purpose is to give Claude Code the context it needs to contribute effectively.

---

## Project Summary

**HotPass** is a lightweight desktop password utility built in Python.
It allows a user to activate a password for a fixed duration and type it
into any active field using a global keyboard shortcut, without ever
touching the system clipboard.

Full user-facing documentation is in `README.md`.
This file covers the internal technical context Claude Code needs.

---

## Core Behavior to Understand Before Touching Anything

- The password is **never copied to the clipboard**. It is typed directly
  using `keyboard.write()`. This is intentional and must not be reverted.
- The hotkey (`Ctrl+Alt+P`) is **only active when the user has clicked Activate**.
  Outside that window, pressing the shortcut does nothing.
- The session has a **configurable timer** (15min, 30min, 1h, 4h). When it
  expires, the session auto-deactivates and a popup notifies the user.
- The password input field is **locked (disabled)** while a session is active.
  It unlocks only on Deactivate or expiry.
- Everything lives in **RAM only**. Nothing is written to disk. No database,
  no config file, no encrypted store.

---

## Architecture

The project is split into three layers. Each layer has a single responsibility
and must not reach into the others beyond its defined interface.

### Layer 1 — Configuration (`config.py`)
Holds all constants: hotkey string, timer duration options, GUI theme,
refresh interval, and typing delay. No logic, no imports from other layers.
If you need to change a constant, change it here only.

### Layer 2 — Core Logic (`core/`)
Two modules, no GUI dependencies allowed in either:

**`core/password_manager.py`**
Owns the session state: whether a password is active, when it expires,
and how much time remains. Exposes `activate()`, `deactivate()`,
`is_expired()`, `get_remaining_time()`, and `check_and_auto_deactivate()`.
The `timer_duration` attribute is set externally by `main.py` before
calling `activate()`, based on the user's dropdown selection.

**`core/hotkey_handler.py`**
Registers and unregisters the global hotkey using the `keyboard` library.
On hotkey press, it checks session state, then launches a daemon thread
that waits briefly (to allow focus to shift) and calls `keyboard.write()`
with the password. It must never import PySimpleGUI or interact with the UI.

### Layer 3 — Interface (`main.py`)
Builds the PySimpleGUI window, runs the event loop, connects user actions
to the core logic, and updates the UI on each tick (every 500ms via timeout).
This is the only file allowed to import PySimpleGUI.

---

## File Map

```
hotpass/
├── main.py                  # GUI + event loop + orchestration
├── config.py                # All constants (edit here, nowhere else)
├── core/
│   ├── __init__.py          # Empty, required for module resolution
│   ├── password_manager.py  # Session state and timer
│   └── hotkey_handler.py    # Hotkey listener and keyboard.write()
├── requirements.txt         # PySimpleGUI, keyboard
├── assets/
│   └── screenshot.png       # UI screenshot for README
├── README.md                # User-facing documentation (EN)
├── README.es.md             # User-facing documentation (ES)
└── CLAUDE.md                # This file
```

---

## Dependencies

Only two runtime dependencies:

- **PySimpleGUI** — GUI framework. Uses the event loop pattern with a
  `timeout` value so the UI refreshes the timer and progress bar
  without blocking.
- **keyboard** — global hotkey registration and direct text injection.
  Requires Administrator on Windows. Requires Xorg (not Wayland) on Linux.

No database libraries. No encryption libraries. No clipboard libraries.
If a proposed change requires adding a new dependency, evaluate carefully
whether it is truly necessary.

---

## Threading Model

Two threads run simultaneously after startup:

1. **Main thread** — PySimpleGUI event loop. Handles all UI updates,
   button events, and timer checks.
2. **Daemon thread** (spawned on hotkey press) — executes `keyboard.write()`
   with a brief sleep before typing to allow the OS to shift focus away
   from the app window.

The `PasswordManager` instance is shared between both threads.
No lock is used. Access is limited to simple attribute reads and writes,
which are atomic in CPython. Do not introduce complex shared state
without adding proper synchronization.

---

## Key Constraints

- **Do not reintroduce clipboard usage.** The original script used
  `pyperclip` + `pyautogui`. This was replaced with `keyboard.write()`
  specifically to avoid `Win+V` history exposure. Any regression here
  is a security issue.
- **Do not add persistent storage** unless explicitly requested by the
  maintainer. The in-RAM design is intentional.
- **Do not import PySimpleGUI outside `main.py`.** Core logic must remain
  GUI-agnostic for testability and portability.
- **Do not use `suppress=True`** in `keyboard.add_hotkey()`. It caused
  the hotkey to stop working on Windows. The current setting is
  `suppress=False`.
- **The `timer_duration` attribute** on `PasswordManager` must be set
  before calling `activate()`. It is not a constructor argument; it is
  set dynamically by `main.py` based on the dropdown selection.

---

## Known Platform Issues

| Issue | Platform | Status |
|-------|----------|--------|
| Wayland blocks global hotkeys | Ubuntu | Won't fix — use Xorg |
| `keyboard` needs Administrator | Windows | Known, documented |
| `keyboard.write()` may fail on uncommon Unicode | Both | Known limitation |
| `suppress=True` breaks hotkey registration | Windows | Fixed (use `suppress=False`) |

---

## How to Run Locally

```
1. Create a virtual environment with uv or pip
2. Install requirements.txt
3. Run main.py directly or via uv run
4. On Windows, run as Administrator if hotkey does not respond
5. On Ubuntu, ensure the session type is Xorg, not Wayland
```

---

## How to Build the Executable

```
1. Install pyinstaller as a dev dependency
2. Run pyinstaller with --onefile --windowed flags
3. Output lands in dist/
4. Do not commit dist/ or build/ to the repository
5. Distribute the .exe via GitHub Releases, not via the repository tree
```

---

## Pending Features (Roadmap)

These have been discussed but not implemented. If picking one up,
read this file and the README carefully before starting.

- **System tray support** — minimize to tray instead of taskbar.
  Requires `pystray` + `Pillow`. Non-trivial interaction with the
  PySimpleGUI event loop.
- **Multiple passwords** — store more than one password with labels.
  Would require a list/dict in `PasswordManager` and UI changes in `main.py`.
- **Sound on paste** — a short beep when `keyboard.write()` completes.
- **Auto-start on login** — register the app in the OS startup sequence.

---

## What Claude Code Should NOT Do

- Do not refactor working code without a clear reason
- Do not add abstractions that are not needed yet
- Do not change the hotkey from `Ctrl+Alt+P` unless explicitly asked
- Do not add logging frameworks — `print()` is sufficient for this project
- Do not generate unit tests unless asked — the project is tested manually
- Do not modify `CLAUDE.md` or `README.md` during feature work unless
  the task explicitly includes documentation updates

---

## Summary for Quick Orientation

> HotPass is a small, focused tool. Two dependencies. Three layers.
> One hotkey. No clipboard. No disk writes. Keep it simple.