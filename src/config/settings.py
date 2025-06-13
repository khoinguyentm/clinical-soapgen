from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EVALUATION_DATA_DIR = DATA_DIR / "evaluation"

# Input directories
AUDIO_DIR = RAW_DATA_DIR / "audio"
TRANSCRIPT_DIR = RAW_DATA_DIR / "transcripts"
NOTES_DIR = RAW_DATA_DIR / "notes"
TEXTGRID_DIR = RAW_DATA_DIR / "textgrid"

# Output directories
OUTPUT_DIR = ROOT_DIR / "output"
JOINED_TRANSCRIPTS_DIR = PROCESSED_DATA_DIR / "joined_transcripts"
TRAINING_DATA_DIR = PROCESSED_DATA_DIR / "training_data"

# Model settings
MODEL_NAME = "mistral"
PROMPT_TEMPLATE = """Below is a conversation between a doctor and a patient.

Transcript:
{transcript}

Generate a SOAP note from this conversation."""

# SOAP note settings
REQUIRED_SECTIONS = ["Subjective", "Objective", "Assessment", "Plan"]

# Create directories if they don't exist
for directory in [
    DATA_DIR,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    EVALUATION_DATA_DIR,
    AUDIO_DIR,
    TRANSCRIPT_DIR,
    NOTES_DIR,
    TEXTGRID_DIR,
    OUTPUT_DIR,
    JOINED_TRANSCRIPTS_DIR,
    TRAINING_DATA_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True) 