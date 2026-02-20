from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

from yt_dlp import YoutubeDL

CONFIG_PATH = Path.home() / ".youtube_music_downloader_config.json"

LogFn = Callable[[str], None]


def default_config() -> dict[str, Any]:
    return {
        "playlist_url": "",
        "output_dir": str((Path.cwd() / "downloads").resolve()),
        "archive_file": ".download_archive.txt",
        "audio_format": "m4a",
        "audio_quality": "0",
        "cookies_from_browser": "",
    }


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return default_config()

    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        cfg = default_config()
        cfg.update(data)
        return cfg
    except Exception:
        return default_config()


def save_config(config: dict[str, Any]) -> None:
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")


def resolve_config(raw: dict[str, Any]) -> dict[str, Any]:
    resolved = default_config()
    resolved.update(raw)

    output_dir = Path(str(resolved["output_dir"])).expanduser().resolve()
    resolved["output_dir"] = str(output_dir)

    archive_path = Path(str(resolved["archive_file"])).expanduser()
    if not archive_path.is_absolute():
        archive_path = output_dir / archive_path
    resolved["archive_file"] = str(archive_path.resolve())

    return resolved


def build_ydl_opts(config: dict[str, Any], log: LogFn) -> dict[str, Any]:
    class Logger:
        def debug(self, msg: str) -> None:
            if msg and not msg.startswith("[debug]"):
                log(msg)

        def warning(self, msg: str) -> None:
            if msg:
                log(f"WARNING: {msg}")

        def error(self, msg: str) -> None:
            if msg:
                log(f"ERROR: {msg}")

    def hook(status: dict[str, Any]) -> None:
        state = status.get("status")
        filename = status.get("filename", "")
        if state == "downloading":
            speed = status.get("_speed_str", "")
            eta = status.get("_eta_str", "")
            pct = status.get("_percent_str", "")
            if pct:
                log(f"Downloading {pct.strip()} {speed} ETA {eta} :: {Path(filename).name}")
        elif state == "finished":
            log(f"Downloaded: {Path(filename).name}")

    opts: dict[str, Any] = {
        "ignoreerrors": True,
        "format": "bestaudio/best",
        "outtmpl": str(Path(config["output_dir"]) / "%(playlist_index|)03d - %(title)s.%(ext)s"),
        "download_archive": config["archive_file"],
        "writethumbnail": True,
        "embedthumbnail": True,
        "addmetadata": True,
        "concurrent_fragment_downloads": 8,
        "retries": 10,
        "extractor_retries": 5,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": config["audio_format"],
                "preferredquality": config["audio_quality"],
            },
            {"key": "FFmpegMetadata"},
            {"key": "EmbedThumbnail"},
        ],
        "parse_metadata": ["%(artist,uploader)s:%(artist)s"],
        "logger": Logger(),
        "progress_hooks": [hook],
        "noprogress": True,
    }

    cookies_from_browser = str(config.get("cookies_from_browser", "")).strip()
    if cookies_from_browser:
        opts["cookiesfrombrowser"] = (cookies_from_browser,)

    return opts


def run_download(config: dict[str, Any], log: LogFn) -> tuple[bool, str]:
    cfg = resolve_config(config)
    if not cfg["playlist_url"]:
        return False, "Playlist URL is required."

    output_dir = Path(cfg["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    log(f"Playlist: {cfg['playlist_url']}")
    log(f"Output folder: {cfg['output_dir']}")
    log(f"Archive file: {cfg['archive_file']}")

    try:
        with YoutubeDL(build_ydl_opts(cfg, log)) as ydl:
            ydl.download([cfg["playlist_url"]])
    except Exception as exc:
        return False, f"Download failed: {exc}"

    return True, "Sync complete. Already-downloaded songs were skipped automatically."
