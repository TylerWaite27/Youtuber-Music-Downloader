from __future__ import annotations

from flask import Flask, redirect, render_template, request, url_for

from downloader_core import load_config, resolve_config, run_download, save_config

app = Flask(__name__)


def form_to_config(form: dict[str, str]) -> dict[str, str]:
    return {
        "playlist_url": form.get("playlist_url", "").strip(),
        "output_dir": form.get("output_dir", "").strip(),
        "archive_file": form.get("archive_file", "").strip(),
        "audio_format": form.get("audio_format", "m4a").strip() or "m4a",
        "audio_quality": form.get("audio_quality", "0").strip() or "0",
        "cookies_from_browser": form.get("cookies_from_browser", "").strip(),
    }


@app.get("/")
def index():
    config = resolve_config(load_config())
    return render_template("index.html", config=config, logs=[], status=None, message="")


@app.post("/sync")
def sync():
    submitted = form_to_config(request.form)
    config = resolve_config(submitted)

    if "save_defaults" in request.form:
        save_config(config)

    logs: list[str] = []

    def push(line: str) -> None:
        logs.append(line)

    success, message = run_download(config, push)
    status = "success" if success else "error"
    return render_template("index.html", config=config, logs=logs[-250:], status=status, message=message)


@app.post("/reset-defaults")
def reset_defaults():
    save_config(resolve_config({}))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
