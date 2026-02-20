#!/usr/bin/env python3
from __future__ import annotations

import argparse

from downloader_core import load_config, resolve_config, run_download, save_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="YouTube Music playlist downloader")
    parser.add_argument("--playlist-url")
    parser.add_argument("--output-dir")
    parser.add_argument("--archive-file")
    parser.add_argument("--audio-format", choices=["m4a", "mp3"])
    parser.add_argument("--audio-quality")
    parser.add_argument("--cookies-from-browser")
    parser.add_argument("--save-defaults", action="store_true")
    parser.add_argument("--show-config", action="store_true")
    parser.add_argument("--reset-config", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if args.reset_config:
        save_config(resolve_config({}))
        print("Defaults reset.")
        return 0

    config = load_config()
    for key in [
        "playlist_url",
        "output_dir",
        "archive_file",
        "audio_format",
        "audio_quality",
        "cookies_from_browser",
    ]:
        value = getattr(args, key)
        if value:
            config[key] = value

    config = resolve_config(config)

    if args.show_config:
        for key, value in config.items():
            print(f"{key}: {value}")
        return 0

    if args.save_defaults:
        save_config(config)

    lines: list[str] = []

    def log(message: str) -> None:
        lines.append(message)
        print(message)

    success, message = run_download(config, log)
    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
