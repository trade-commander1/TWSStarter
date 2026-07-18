# AGENTS.md — TWSStarter

Guidance for AI coding agents (and humans) working on this repository.

## What this is

TWSStarter is a **PyQt6 desktop launcher for Interactive Brokers Trader
WorkStation (TWS) and IB Gateway**. It starts TWS/Gateway, auto-fills the login,
shows which instances are running, and can start/stop several at once.

It is a *convenience launcher* — it does **not** auto-start TWS, keep it running,
or restart it, and it is **not** real monitoring (it only reports status). For a
24/5 session, users are pointed at TWS's own Auto Restart. Keep this framing
accurate in code, help and docs.

Independent project; not affiliated with Interactive Brokers. Licensed MIT.

## Tech stack & platforms

- **Python 3.13+**, **PyQt6**, `cryptography`, `pyautogui`, `pywinauto`.
- Dependency/venv management: **`uv`**.
- **Windows is the primary target.** The UI and launching work cross-platform,
  but **autofill and runtime monitoring are Windows-only** (they use the Win32
  API via `win32gui`/`pyautogui`). A Linux build is produced but those features
  no-op there.

## Run & build

```bash
uv sync                            # create venv, install deps
uv run python -m twsstarter.main   # run from source (or run.bat on Windows)
```

- **Windows package:** `build/build_windows.bat` → `dist/TWSStarter.exe` and, if
  Inno Setup 6 is installed, `dist/TWSStarter-<ver>-Setup.exe`.
  The `.exe`/installer icon comes from `build/TWSStarter.ico` (regenerate with
  `build/make_ico.py` when the icon changes).
- **Linux package:** `build/build_linux.sh` → single binary + `.tar.gz` in
  `dist/`. Run it on Linux/WSL.

**Critical build gotcha — isolate virtualenvs per platform.** When building for
both Windows and Linux from the same working tree (e.g. Windows + WSL over a
shared path), each platform must use its own venv or they clobber each other
(`.venv/Scripts` vs `.venv/bin`). In WSL always
`export UV_PROJECT_ENVIRONMENT=.venv-linux`; Windows keeps `.venv`. Run the two
builds **sequentially** (they share `uv.lock`). **Never rename a venv** — console
scripts keep a hardcoded interpreter shebang and break; delete and re-`uv sync`.

## Versioning (strict — read before releasing)

`src/twsstarter/version.py` is the **single source of truth**: `VERSION` (X.Y)
and `BUILD` (Z). The build scripts read it, so packages stay in sync.

- New feature / architectural / functional change → bump `VERSION`, reset
  `BUILD` to 0.
- Bugfix / refactor / minor change → bump `BUILD`.
- The full version is shown in the main window title bar (`title_string()`).
- **Recurring mistake to avoid:** when adding a changelog line, also change the
  `BUILD`/`VERSION` **constant** — not just the docstring history. Forgetting it
  produces a wrongly-numbered installer. Always edit constant + changelog
  together, and verify the produced installer filename.

## Repository layout

```
src/twsstarter/
  main.py            entry point: Qt setup, language, migration, first-run
                     disclaimer, then MainWindow
  version.py         VERSION/BUILD + version/title strings (source of truth)
  models.py          ConnectionEntry / AppSettings (+ JSON (de)serialization)
  storage.py         config.json persistence, migrate_encryption(), legacy
                     data.json migration
  crypto.py          machine-bound credential encryption (see below)
  launcher.py        start TWS/Gateway; passes is_gateway to autofill
  autofill.py        fill the login dialog (Windows; pyautogui/win32)
  process_scan.py    system-wide TWS/Gateway detection (Windows)
  runtime_monitor.py background status thread (running/starting/stopped)
  tracing.py         GUI trace feed + rotating file log
  paths.py           per-user data/log dirs
  i18n/              strings.py (translations + help) and the tr()/language API
  resources/         icon.py, flags.py, help_images.py (generated), exe_icons.py
  ui/                main_window, connection_card, connection_dialog,
                     settings_dialog, about_dialog, disclaimer_dialog,
                     help_browser, theme, trace_panel
build/               PyInstaller spec, Inno Setup script, build & asset scripts
res/                 screenshots used in README/help
```

## Architecture notes

- **Credential encryption (`crypto.py`).** Passwords are encrypted with Fernet
  using a key derived from a **stable per-machine identifier — the Windows
  MachineGuid** (not `uuid.getnode()`, which changes with network adapters and
  broke decryption historically). `reencrypt_legacy()` + `migrate_encryption()`
  transparently migrate tokens from the old host+MAC key at startup. Config
  cannot be decrypted on a different machine (by design).
- **Launch & autofill.** `launcher.launch_tws/launch_gateway` know the mode and
  pass `is_gateway` to `autofill.start_thread`, so login-window detection does
  **not** depend on the localized window title. TWS login is matched by known
  titles (`Login`, `Anmelden`, …) **or** the Java/Swing window class (`SunAwt…`)
  as a language-independent fallback; Gateway by its (non-localized) product
  title. Autofill uses simulated clicks/keystrokes — keep the login window
  visible.
- **Status detection.** `process_scan.scan_running()` finds TWS by window-title
  regex and Gateway by a listening API port; `runtime_monitor` runs a background
  thread and emits a 3-state status per connection (running/starting/stopped).
  It is status-only — it never restarts anything. Invariant to preserve: each
  running instance is attributed to **at most one** connection (claimed by PID),
  and a learned TWS account id is assigned to only one connection — otherwise a
  single TWS would be counted twice when connections share an account.
- **Autostart (watchdog).** Independent of the monitor: `MainWindow` runs a
  repeating `QTimer` every `AppSettings.check_interval` seconds (default 30, also
  the delay before the first check). Each tick (re)starts, in its default mode,
  every connection with `ConnectionEntry.autostart` on that is not currently
  active — so a closed connection comes back while the switch stays on. This is
  the *only* part that launches processes on its own; `runtime_monitor` does not.
- **Storage.** Everything lives in `%LocalAppData%\TWSStarter\config.json`; logs
  under `…\log`. `AppSettings.disclaimer_accepted` gates the first-run notice;
  `AppSettings.check_interval` drives the autostart watchdog;
  `ConnectionEntry.autostart` (default on) enables it per connection.

## Internationalization (`i18n/strings.py`)

- **`LANGUAGES` is the single source of truth** for the *selectable* set (the 10
  languages TWS ships in: en, de, fr, es, it, ru, nl, pt, zh, ja).
  `i18n.set_language`/`detect_language` gate on `LANGUAGES`; leftover translation
  data for other languages (if any) is inert. The language menu is built from
  `LANGUAGES` and shows a painted national flag per language (`resources/flags`)
  — **not** emoji flags (Windows renders those as letters).
- Translation data: `STRINGS` (main UI) merged with `_EXTRA`; help text in
  `_HELP_CURRENT` (overrides the legacy `_HELP`). All keyed by language code.
- **Help is HTML shown in the external browser** via
  `help_browser.open_help_in_browser` (writes a temp file). `ui/help_dialog.py`
  (an in-app QTextBrowser) exists but is currently **unused**.
- **Help screenshots** are embedded inline as base64 data URIs. A post-build loop
  in `strings.py` inserts, per language and by section order (language-
  independent), a top callout box, a Settings section, an honest status heading,
  and `[[IMG:main|add|settings]]` tokens; `help_browser` swaps the tokens for
  `<img>` using `resources/help_images.DATA_URIS`.
- When you change UI strings that appear in help, keep all 10 languages in sync.

## Dev/asset tooling (`build/`)

- `make_ico.py` — regenerate `build/TWSStarter.ico` from `resources/icon.py`.
- `make_screens.py [lang]` — render every window to `res/ui_*.png`. **Must run on
  the native Qt platform** (real fonts); the offscreen platform renders text as
  empty boxes.
- `make_help_images.py` — encode `res/ui_*.png` into
  `src/twsstarter/resources/help_images.py` (base64 data URIs). Run after
  regenerating screenshots.

## Conventions

- **Comments/docs/identifiers in English**; production-quality, well-commented.
- Match existing style; prefer the simplest working solution (no
  over-engineering). Keep modules focused; add concise module docstrings.
- Verify UI changes headless where possible (`QT_QPA_PLATFORM=offscreen`,
  `widget.grab()` / signal checks); use the native platform when real fonts or
  screenshots are needed.
- Common gotchas: `netstat`/subprocess `.stdout` can be `None` (guard before
  `.splitlines()`); QMessageBox button order is style-driven (use a custom
  `QDialog` when exact placement matters); offscreen Qt has no fonts.
