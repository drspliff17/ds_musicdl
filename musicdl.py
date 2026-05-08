import os
import sys
import shutil
import tempfile
from pathlib import Path

import requests
from yt_dlp import YoutubeDL
import eyed3
import re


def get_input(prompt, default=None):
    val = input(prompt).strip()
    if not val and default is not None:
        return default
    return val


def validate_url(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.status_code < 400
    except Exception:
        return False


def get_ffmpeg_path() -> str:
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base_path = Path(__file__).parent

    ffmpeg_name = "ffmpeg.exe" if sys.platform.startswith("win") else "ffmpeg"

    return str(base_path / ffmpeg_name)


def download_audio(url: str, outdir: Path):
    from typing import Any

    ydl_opts: dict[str, Any] = {
        "format": "bestaudio/best",
        "outtmpl": str(outdir / "%(title)s.%(ext)s"),
        "ffmpeg_location": get_ffmpeg_path(),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
        ydl.download([url])


def fix_filenames(directory: Path):
    for file in directory.glob("*.mp3"):
        name = file.stem

        if "(" in name:
            name = name.split("(")[0]
        elif "[" in name:
            name = name.split("[")[0]

        name = name.replace(".mp3", "")
        name = re.sub(r"[^a-zA-Z0-9 \-]", "", name)
        name = re.sub(r"\s+", " ", name).strip()
        name = name.replace(" ", "_")

        new_path = file.with_name(name + ".mp3")
        file.rename(new_path)


def tag_files(directory: Path, artist: str, album: str):
    for file in directory.glob("*.mp3"):
        audio = eyed3.load(str(file))

        if audio is None:
            continue

        if audio.tag is None:
            audio.initTag()

        tag = audio.tag
        if tag is None:
            continue

        tag.artist = artist
        tag.album = album
        tag.title = file.stem.replace("_", " ")

        tag.save()  # type: ignore[attr-defined]


def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    assume_artist = sys.argv[2] if len(sys.argv) > 2 else None

    if not url:
        url = get_input("[INIT] Please enter URL: ")

    if not url or not validate_url(url):
        print("[ERROR] Invalid URL")
        sys.exit(1)

    target_dir = get_input("[INIT] Target directory (blank = CWD): ", os.getcwd())
    target_dir = Path(target_dir)

    if not target_dir.exists():
        print("[ERROR] Directory does not exist")
        sys.exit(1)

    if assume_artist:
        artist = Path.cwd().name.replace("_", " ")
    else:
        artist = get_input("[INIT] Artist Name: ")

    if not artist:
        print("[ERROR] Artist Name required")
        sys.exit(1)

    album = get_input("[INIT] Album Name: ")
    if not album:
        print("[ERROR] Album required")
        sys.exit(1)

    tmpdir = Path(tempfile.mkdtemp())

    try:
        print("[INFO] Downloading...")
        download_audio(url, tmpdir)

        print("[INFO] Fixing filenames...")
        fix_filenames(tmpdir)

        print("[INFO] Tagging files...")
        tag_files(tmpdir, artist, album)

        print("[INFO] Moving files...")
        for f in tmpdir.glob("*.mp3"):
            shutil.move(str(f), target_dir / f.name)

        print("[FINISHED]")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
