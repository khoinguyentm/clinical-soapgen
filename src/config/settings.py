from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Data directories (based on actual project structure)
AUDIO_DIR = ROOT_DIR / "audio"
TRANSCRIPT_DIR = ROOT_DIR / "transcripts"
NOTES_DIR = ROOT_DIR / "notes"

# Output directories
OUTPUT_DIR = ROOT_DIR / "output"
JOINED_TRANSCRIPTS_DIR = OUTPUT_DIR / "joined_transcripts"
TRAINING_DATA_DIR = OUTPUT_DIR / "training_data"
EVALUATION_DATA_DIR = ROOT_DIR / "human_eval_data"

# Model settings
MODEL_NAME = "mistral"
PROMPT_TEMPLATE = """Below is a conversation between a doctor and a patient.

Transcript:
{transcript}

Generate a SOAP note from this conversation."""

# SOAP note settings
REQUIRED_SECTIONS = ["Subjective", "Objective", "Assessment", "Plan"]

# Create output directories if they don't exist
for directory in [
    OUTPUT_DIR,
    JOINED_TRANSCRIPTS_DIR,
    TRAINING_DATA_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True) 