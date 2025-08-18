"""Transcript processing utilities."""

import re
from pathlib import Path
from typing import Dict, List, Tuple


class TranscriptProcessor:
    """Handles processing and pairing of transcripts with clinical notes."""
    
    def __init__(self, transcript_dir: Path, notes_dir: Path):
        self.transcript_dir = Path(transcript_dir)
        self.notes_dir = Path(notes_dir)
        
    def split_soap_sections(self, note_text: str) -> Dict[str, str]:
        """Parse SOAP-formatted note into sections.
        
        Args:
            note_text: Raw SOAP note text
            
        Returns:
            Dictionary with Subjective, Objective, Assessment, Plan sections
        """
        soap = {"Subjective": "", "Objective": "", "Assessment": "", "Plan": ""}
        current_section = None

        for line in note_text.splitlines():
            line = line.strip()
            if line.lower().startswith("subjective"):
                current_section = "Subjective"
            elif line.lower().startswith("objective"):
                current_section = "Objective"
            elif line.lower().startswith("assessment"):
                current_section = "Assessment"
            elif line.lower().startswith("plan"):
                current_section = "Plan"
            elif current_section:
                soap[current_section] += line + " "
        
        return soap
        
    def pair_transcripts_and_notes(self) -> List[Tuple[str, Dict[str, str]]]:
        """Pair transcript files with their corresponding SOAP notes.
        
        Returns:
            List of (transcript, soap_sections) tuples
        """
        print("Pairing transcripts with SOAP notes...")
        pairs = []
        
        transcript_files = sorted(self.transcript_dir.glob("*.txt"))
        note_files = sorted(self.notes_dir.glob("*.txt"))

        # Create mapping from filename stem to note file
        note_dict = {note.stem.lower(): note for note in note_files}
        print(f"Found {len(transcript_files)} transcripts and {len(note_dict)} notes.")

        for transcript_file in transcript_files:
            t_stem = transcript_file.stem.lower()
            
            if t_stem in note_dict:
                print(f"✅ Match: {transcript_file.name} ↔ {note_dict[t_stem].name}")
                note_file = note_dict[t_stem]
                
                transcript = transcript_file.read_text(encoding="utf-8")
                note = note_file.read_text(encoding="utf-8")
                soap = self.split_soap_sections(note)
                pairs.append((transcript, soap))
            else:
                print(f"❌ No match for: {transcript_file.name}")

        print(f"Paired {len(pairs)} transcript-note files.")
        return pairs
        
    def validate_soap_structure(self, text: str, required_sections: List[str] = None) -> bool:
        """Check if text contains all required SOAP sections.
        
        Args:
            text: Text to validate
            required_sections: List of required section names
            
        Returns:
            True if all sections are present
        """
        if required_sections is None:
            required_sections = ["Subjective", "Objective", "Assessment", "Plan"]
            
        return all(
            re.search(rf"(?i)\b{section}\b", text) 
            for section in required_sections
        )
        
    def extract_span_mentions(
        self, 
        transcript: str, 
        section_text: str, 
        top_n: int = 5
    ) -> List[str]:
        """Extract most relevant transcript sentences for a SOAP section.
        
        Args:
            transcript: Original conversation transcript
            section_text: SOAP section text
            top_n: Number of top matching sentences to return
            
        Returns:
            List of most relevant transcript sentences
        """
        transcript_sentences = transcript.split(".")
        section_words = set(section_text.lower().split())
        ranked = []
        
        for sentence in transcript_sentences:
            sentence_words = set(sentence.lower().split())
            overlap = len(section_words.intersection(sentence_words))
            ranked.append((overlap, sentence.strip()))
            
        ranked.sort(reverse=True)
        return [s for _, s in ranked[:top_n] if s]