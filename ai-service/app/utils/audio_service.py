import subprocess
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
import shutil

TEMP_DIR = Path("/samples").resolve()
TEMP_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_MIME_TYPES = {"audio/mpeg", "audio/mp4", "audio/ogg", "audio/flac", "audio/wav", "audio/x-m4a"}
ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".ogg", ".flac", ".wav", ".m4a"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


async def save_upload(file: UploadFile) -> Path:
    """Validate and save an uploaded file with a server-generated name."""

    # Validate MIME type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")

    # Validate extension from original filename (for defense-in-depth, not trust)
    original_suffix = Path(file.filename).suffix.lower() if file.filename else ""
    if original_suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file extension: {original_suffix}")

    # Generate a safe, random filename — never use the client-supplied name
    safe_filename = f"{uuid.uuid4().hex}{original_suffix}"
    dest_path = TEMP_DIR / safe_filename

    # Stream to disk while enforcing size limit
    size = 0
    try:
        with dest_path.open("wb") as f:
            async for chunk in file:
                size += len(chunk)
                if size > MAX_FILE_SIZE:
                    raise HTTPException(status_code=413, detail="File too large")
                f.write(chunk)
    except Exception:
        dest_path.unlink(missing_ok=True)  # clean up partial file
        raise

    return dest_path


def convert_to_wav(input_path: Path) -> Path:
    """Convert a server-controlled path to WAV. Never call with user-supplied paths."""

    # Double-check the path is still within our temp dir (defence against symlinks etc.)
    try:
        input_path.resolve().relative_to(TEMP_DIR)
    except ValueError:
        raise ValueError("Input path is outside the allowed directory")

    output_path = input_path.with_suffix(".wav")

    command = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-ac", "1",
        "-ar", "16000",
        str(output_path),
    ]

    result = subprocess.run(  # noqa: S603
        command,
        check=True,
        shell=False,
        capture_output=True,
        timeout=120,  # don't let ffmpeg hang forever
    )

    return output_path


def cleanup(*paths: Path) -> None:
    """Remove temp files after processing."""
    for p in paths:
        p.unlink(missing_ok=True)