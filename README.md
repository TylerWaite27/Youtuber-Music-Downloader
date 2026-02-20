# YouTube Music Liked Playlist Downloader (Simple App)

This project gives you a **simple local app** to download your YouTube Music liked playlist.

It will:
- download songs,
- keep title/artist metadata,
- embed cover art,
- skip songs that were already downloaded before.

---

## Super simple setup (Windows)

1. Install **Python 3.10+** from: https://www.python.org/downloads/
   - During install, check **"Add Python to PATH"**.
2. Install **FFmpeg** (needed for cover art + metadata):
   - Download from: https://ffmpeg.org/download.html
   - Make sure `ffmpeg` works in Command Prompt:
     ```bat
     ffmpeg -version
     ```
3. Download this repository as ZIP from GitHub, then extract it.
4. Open the extracted folder.
5. Double-click **`start_app.bat`**.
6. Your browser should open to:
   - `http://127.0.0.1:5000`

---

## Super simple setup (Mac / Linux)

1. Install **Python 3.10+**.
2. Install **FFmpeg**.
3. Download/extract this repository.
4. Open Terminal in the project folder.
5. Run:

```bash
./start_app.sh
```

6. Open:
- `http://127.0.0.1:5000`

---

## How to use the app

1. In the app page, paste your YouTube Music playlist URL.
2. Pick the output folder where songs should be saved.
3. Leave other settings as default unless you need to change them.
4. Click **Sync Playlist**.
5. Wait for completion.

Next time, run app again and click sync — it will only download new songs.

---

## If your liked playlist is private

In the app field **Cookies from browser**, type your browser name, for example:
- `chrome`
- `firefox`
- `edge`

Then click **Sync Playlist**.

---

## Exactly what files to keep

Keep these files together in one folder:
- `app.py`
- `downloader_core.py`
- `requirements.txt`
- `templates/` folder
- `static/` folder
- `start_app.bat` (Windows helper)
- `start_app.sh` (Mac/Linux helper)

---

## Manual commands (if helper script is not used)

In the project folder:

```bash
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.

---

## Common question: “Will GitHub auto-update on my PC?”

- GitHub updates when new commits are pushed online.
- Your local folder does **not** auto-update.
- If you used `git clone`, run:

```bash
git pull
```

- If you downloaded ZIP, download a new ZIP when you want latest changes.
