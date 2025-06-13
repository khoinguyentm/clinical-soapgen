import re
from typing import Dict, List, Tuple

from ..config import settings

def split_soap_sections(note_text: str) -> Dict[str, str]:
    """Split a SOAP-formatted note into its sections.
    
    Args:
        note_text: The full text of the SOAP note
        
    Returns:
        Dictionary with keys for each SOAP section and their content
    """
    soap = {section: "" for section in settings.REQUIRED_SECTIONS}
    current_section = None

    for line in note_text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        for section in settings.REQUIRED_SECTIONS:
            if line.lower().startswith(section.lower()):
                current_section = section
                break
                
        if current_section:
            soap[current_section] += line + " "
    
    return soap

def pair_transcripts_and_notes() -> List[Tuple[str, Dict[str, str]]]:
    """Pair transcripts with their corresponding SOAP notes.
    
    Returns:
        List of tuples containing (transcript, soap_sections)
    """
    print("Pairing transcripts with SOAP notes...")
    pairs = []
    
    transcript_files = sorted(settings.JOINED_TRANSCRIPTS_DIR.glob("*.txt"))
    note_files = sorted(settings.NOTES_DIR.glob("*.txt"))

    # Dict mapping stem (e.g. "day1_consultation01") to Path
    note_dict = {note.stem.lower(): note for note in note_files}
    print(f"Found {len(transcript_files)} transcripts and {len(note_dict)} notes.")

    for transcript_file in transcript_files:
        t_stem = transcript_file.stem.lower()
        
        if t_stem in note_dict:
            print(f"✅ Match: {transcript_file.name} ↔ {note_dict[t_stem].name}")
            note_file = note_dict[t_stem]
            transcript = transcript_file.read_text(encoding="utf-8")
            note = note_file.read_text(encoding="utf-8")
            soap = split_soap_sections(note)
            pairs.append((transcript, soap))
        else:
            print(f"❌ No match for: {transcript_file.name}")

    print(f"Paired {len(pairs)} transcript-note files.")
    return pairs 