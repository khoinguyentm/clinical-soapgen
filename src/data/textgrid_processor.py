import subprocess
from pathlib import Path
from typing import List

from ..config import settings

def convert_textgrid_to_transcripts() -> None:
    """Convert TextGrid files to transcript files."""
    print("Converting TextGrid files to transcripts...")
    subprocess.run([
        "python", "scripts/textgrid_to_transcript.py",
        f"--transcript_path={settings.TRANSCRIPT_DIR}",
        f"--output_path={settings.JOINED_TRANSCRIPTS_DIR}"
    ])

def extract_utterances() -> None:
    """Extract utterances from transcripts and align with audio."""
    print("Extracting utterances from transcripts...")
    subprocess.run([
        "python", "scripts/extract_utterances.py",
        f"--audio_path={settings.AUDIO_DIR}",
        f"--transcript_path={settings.TRANSCRIPT_DIR}",
        f"--output_path={settings.OUTPUT_DIR}"
    ]) 