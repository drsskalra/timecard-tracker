"""
Timecard Activity Logger (Windows)
----------------------------------
Records which app / file / email / Teams window is in the foreground, every few
seconds, into one JSONL file per day in your OneDrive. Time Card Tracker's
"Activity Review" panel imports those files so you can map them to projects,
edit, and add them to your timecard.

* No admin rights and no extra packages (pure ctypes, standard library only).
* Logs ONLY the app name + window title (for example "Aerojet 5YR Review.docx - Word").
  No keystrokes, screenshots, or file contents.
* Idle time (no keyboard or mouse for IDLE_LIMIT seconds) and the lock screen are logged as idle.

Run hidden at every logon (no admin needed):
  1. Win+R  ->  shell:startup  -> Enter
  2. New > Shortcut, target:
       "C:\\path\\to\\pythonw.exe" "C:\\path\\to\\activity_logger.py"
  To stop it: Task Manager > end "pythonw.exe".

Author: Shashank Singh Kalra, PhD, PE
"""
import ctypes
import ctypes.wintypes as wt
import datetime as dt
import json
import os
import re
import time

# ---------------- settings ----------------
POLL = 5            # seconds between samples
IDLE_LIMIT = 300    # seconds with no input => idle
MIN_SEG = 15        # don't write segments shorter than this (seconds)
MAX_SEG = 600       # flush long segments every 10 min (limits loss on shutdown)
PRIVATE_HINTS = ("InPrivate", "Incognito", "Private Browsing")
OUT_DIR = os.path.join(
    os.environ.get("OneDriveCommercial") or os.environ.get("OneDrive") or os.path.expanduser("~"),
    "TimecardActivity",
)

APPS = {
    "winword.exe": ("Word", "file"), "excel.exe": ("Excel", "file"),
    "powerpnt.exe": ("PowerPoint", "file"), "onenote.exe": ("OneNote", "file"),
    "acrobat.exe": ("Acrobat", "file"), "acrord32.exe": ("Acrobat", "file"),
    "outlook.exe": ("Outlook", "email"), "olk.exe": ("Outlook", "email"),
    "ms-teams.exe": ("Teams", "teams"), "teams.exe": ("Teams", "teams"),
    "code.exe": ("VS Code", "code"), "arcgispro.exe": ("ArcGIS Pro", "file"),
    "acad.exe": ("AutoCAD", "file"), "msedge.exe": ("Edge", "web"),
    "chrome.exe": ("Chrome", "web"), "explorer.exe": ("File Explorer", "file"),
}
SUFFIX = re.compile(
    r"\s*[-|\u2013\u2014]\s*(Microsoft\s+)?(Word|Excel|PowerPoint|OneNote|Outlook|Teams|"
    r"Visual Studio Code|Edge|Google Chrome|Adobe Acrobat.*|Microsoft Teams|Work|Personal)\s*$",
    re.I,
)

# ---------------- Win32 ----------------
user32 = ctypes.WinDLL("user32", use_last_error=True)
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
user32.GetForegroundWindow.restype = wt.HWND
kernel32.GetTickCount.restype = wt.DWORD
kernel32.OpenProcess.restype = wt.HANDLE


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wt.UINT), ("dwTime", wt.DWORD)]


def idle_seconds() -> float:
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    if not user32.GetLastInputInfo(ctypes.byref(lii)):
        return 0.0
    return ((kernel32.GetTickCount() - lii.dwTime) & 0xFFFFFFFF) / 1000.0


def foreground():
    hwnd = user32.GetForegroundWindow()
    if not hwnd:
        return "", ""
    n = user32.GetWindowTextLengthW(hwnd)
    buf = ctypes.create_unicode_buffer(n + 1)
    user32.GetWindowTextW(hwnd, buf, n + 1)
    pid = wt.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    exe = ""
    h = kernel32.OpenProcess(0x1000, False, pid.value)  # PROCESS_QUERY_LIMITED_INFORMATION
    if h:
        size = wt.DWORD(1024)
        pbuf = ctypes.create_unicode_buffer(1024)
        if kernel32.QueryFullProcessImageNameW(h, 0, pbuf, ctypes.byref(size)):
            exe = os.path.basename(pbuf.value)
        kernel32.CloseHandle(h)
    return exe, buf.value


# ---------------- logic ----------------
def classify(exe: str, title: str):
    app, kind = APPS.get(exe.lower(), (os.path.splitext(exe)[0] or "Unknown", "other"))
    if any(p in title for p in PRIVATE_HINTS):
        title = "(private window)"
    item = SUFFIX.sub("", title).strip() or app
    item = re.sub(r"\s*-\s*\S+@\S+$", "", item)  # drop Outlook account suffix
    item = re.sub(r"^\u25cf\s*|\s*\(\d+\)\s*$|\s*-\s*AutoSaved.*$|\s*-\s*Saved.*$", "", item).strip()
    if kind == "teams" and re.search(r"meeting|call", title, re.I):
        kind = "meeting"
    return app, kind, item


def write(seg):
    if not seg or seg["idle"]:
        return
    sec = int((seg["end"] - seg["start"]).total_seconds())
    if sec < MIN_SEG:
        return
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"activity_{seg['start']:%Y-%m-%d}.jsonl")
    rec = {
        "start": seg["start"].isoformat(timespec="seconds"),
        "end": seg["end"].isoformat(timespec="seconds"),
        "sec": sec, "app": seg["app"], "kind": seg["kind"],
        "item": seg["item"], "title": seg["title"], "exe": seg["exe"],
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def new_seg(start, exe, title, idle):
    app, kind, item = classify(exe, title) if not idle else ("Idle", "idle", "Idle")
    return {"start": start, "end": start, "exe": exe, "title": title,
            "app": app, "kind": kind, "item": item, "idle": idle,
            "key": "__idle__" if idle else f"{exe}|{title}"}


def main():
    seg = None
    while True:
        try:
            now = dt.datetime.now()
            idle_s = idle_seconds()
            exe, title = foreground()
            idle = idle_s >= IDLE_LIMIT or exe.lower() in ("lockapp.exe", "") or not title
            key = "__idle__" if idle else f"{exe}|{title}"

            if seg is None:
                seg = new_seg(now, exe, title, idle)
            elif key != seg["key"] or now.date() != seg["start"].date() \
                    or (now - seg["start"]).total_seconds() >= MAX_SEG:
                cut = now
                if idle and not seg["idle"]:
                    cut = max(seg["start"], now - dt.timedelta(seconds=idle_s))  # back-date idle start
                if now.date() != seg["start"].date():
                    cut = dt.datetime.combine(now.date(), dt.time.min)        # split at midnight
                seg["end"] = cut
                write(seg)
                seg = new_seg(cut, exe, title, idle)
            seg["end"] = now
        except Exception as exc:  # never die silently in the background
            try:
                os.makedirs(OUT_DIR, exist_ok=True)
                with open(os.path.join(OUT_DIR, "logger_errors.txt"), "a", encoding="utf-8") as f:
                    f.write(f"{dt.datetime.now().isoformat()} {exc!r}\n")
            except Exception:
                pass
        time.sleep(POLL)


if __name__ == "__main__":
    main()
