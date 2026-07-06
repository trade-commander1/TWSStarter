"""Central version information for TWSStarter — single source of truth.

Versioning policy (global CLAUDE.md → "Versioning & Build Rules"):
  * VERSION (X.Y): incremented on every new feature / architectural /
    functional change.
  * BUILD (Z): incremented on bugfixes / refactoring / minor adjustments;
    reset to 0 whenever VERSION is incremented.

The Windows installer (build_windows.bat) and the Linux build (build_linux.sh)
read these values and pass them on, so the packages stay in sync with the app.

History:
  1.0 Build 0 — initial release (connections, encryption, autofill, i18n,
                help/about, icon).
  1.1 Build 0 — added background runtime monitoring of TWS/Gateway processes.
  1.2 Build 0 — runtime monitoring rewritten to detect instances system-wide
                via window scan (also finds externally / previously started
                TWS/Gateway), instead of session subprocess handles only.
  1.2 Build 1 — account-id learning by difference (robust against TWS
                re-spawning itself with a new PID); PID correlation alone
                failed to learn the account id.
  1.2 Build 2 — fixed Stop (terminate the real window PID, not the dead
                launcher handle); detection/stop now also match the connection
                name against the master account in the title bar (startswith,
                to avoid false positives on common title words).
  1.2 Build 3 — Gateway autofill: enter the password via Tab navigation + Enter
                (fixed: password landed on "More Options" due to layout shift).
                Runtime monitoring made real & honest: a login dialog no longer
                counts as running; new three-state status (running / starting /
                stopped) driven solely by the window scan — no more optimistic
                "running" that lingered after closing the login dialog.
  1.2 Build 4 — Gateway autofill robustness: ignore the install4j splash via a
                minimum-size check, longer settle time, re-focus the dialog
                before each step, and write a diagnostic log to
                ~/.twsstarter/autofill.log.
  1.3 Build 0 — Gateway runtime detection: a running IB Gateway is now detected
                via the API port and attributed to a connection through the
                per-account settings directory (learned on first launch).
  1.3 Build 1 — Gateway detection fix: the live API port is NOT jts.ini's
                LocalServerPort (paper uses 4002, live 4001). Detect a logged-in
                Gateway as "an ibgateway.exe listening on ANY port" instead — the
                pre-login dialog opens no port, so this also separates login from
                running.
  1.4 Build 0 — Batch control: per-connection checkboxes + All; control row with
                Start TWS / Start Gateway / Start Default / Stop (tooltips); cards
                show the default mode and the live connection type (TWS/Gateway).
                Config moved to %LocalAppData%/TWSStarter/config.json (settings,
                connections, checked state; old data.json migrated). New trace
                panel (black, colored, autoscroll, Clear) + rotating file logs in
                log/ (5 MB, purge >3 days every 6 h).
  1.5 Build 0 — Encryption key hardened: derived from the stable Windows
                MachineGuid instead of platform.node()+uuid.getnode(). The old
                MAC-based key changed whenever network adapters/VMs/VPNs came
                and went (even between processes), making stored passwords
                undecryptable and breaking autofill. Existing tokens are migrated
                automatically at startup (all local MACs are tried). The edit
                dialog now pre-fills the current password so the eye button can
                reveal it.
  1.6 Build 0 — Connection cards: per-card start buttons (Default | TWS |
                Gateway) to launch a single connection directly. Mode badge
                recolored — PAPER red, LIVE green.
  1.6 Build 1 — Card buttons reworked: fixed order [Stop] TWS | Gateway |
                Default; the three start buttons share one width (= Gateway) and
                use the same blue/red colors as the "All" control-row buttons
                (shared START_BTN_CSS/STOP_BTN_CSS in theme.py). Stop retains its
                slot when hidden so the start buttons stay at a fixed position.
  1.6 Build 2 — Autofill language fix: the TWS login window is detected
                independently of UI language. The caller passes is_gateway, so
                the localized title (e.g. "Anmelden" in German) is only a hint;
                for TWS a Java/Swing window-class fallback also matches unlisted
                languages. Runtime detection recognizes the German login title
                too, so a card no longer drops to "stopped" during login.
  1.7 Build 0 — Language set aligned with the languages TWS ships in: English,
                German, French, Spanish, Italian, Russian, Dutch, Portuguese,
                Simplified Chinese, Japanese. Dutch added (UI + help); Polish,
                Turkish and Hindi removed from the selectable set. LANGUAGES is
                now the single source of truth (i18n gates selection/detection
                on it). Close dialog (when instances are still running) gained a
                third option: "Close all & exit" — stop every running instance,
                then quit.
  1.7 Build 1 — New app icon: a subtle "launch" motif (play triangle in a soft
                ring) instead of the candlestick chart, which wrongly suggested
                a stock-market app rather than a launcher.
  1.7 Build 2 — Close dialog reworked into a custom dialog so "Exit anyway" sits
                on the far left, separated from the primary actions. Help (all
                10 languages) refreshed and the Auto Restart guidance expanded:
                to keep TWS/Gateway running around the clock, enable TWS's
                Auto Restart under Configuration → Lock and Exit → Auto Logoff
                Timer, with the correct path from the current TWS UI. Hardened
                _listening_pids() against netstat returning no output (guard
                None) so the runtime-monitor thread can't crash.
  1.8 Build 0 — Language menu shows a national flag before each language (painted
                icons, since Windows doesn't render flag emoji). "Start Default"
                is now the left-most action in both the control row and each card
                (batch and single action). Added a README and module docstrings
                for open-source publishing.
  1.8 Build 1 — Help now embeds UI screenshots (main window + add-connection
                dialog) inline as base64 data URIs, in all 10 languages. New
                dev tools build/make_screens.py (render every window to res/) and
                build/make_help_images.py (encode them into resources/help_images).
  1.8 Build 2 — Help reworked (all 10 languages): a prominent callout box at the
                top makes clear TWSStarter only launches/stops/shows status and
                does NOT auto-start or keep TWS running (use TWS Auto Restart for
                that); added a Settings section (TWS/Gateway install paths) with
                a screenshot; the misleading "monitoring" heading is now honest
                ("which instances are running").
  1.9 Build 0 — First-run disclaimer: an English legal notice shown once on the
                first start; acceptance is stored (settings.disclaimer_accepted).
                Declining/closing exits the app.
"""
from __future__ import annotations

APP_NAME: str = "TWSStarter"
VERSION: str = "1.9"   # X.Y — feature version
BUILD: int = 0         # Z   — build number


def version_string() -> str:
    """Short form, e.g. 'v1.1 Build 0'."""
    return f"v{VERSION} Build {BUILD}"


def title_string() -> str:
    """Full window-title string, e.g. 'TWSStarter v1.1 Build 0'."""
    return f"{APP_NAME} {version_string()}"
