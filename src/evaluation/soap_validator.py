import re
from typing import Dict, List, Tuple

from ..config import settings

class SoapValidator:
    """Validator for checking SOAP note completeness and structure."""
    
    def __init__(self, required_sections: List[str] = settings.REQUIRED_SECTIONS):
        self.required_sections = required_sections
        
    def has_all_sections(self, text: str) -> bool:
        """Check if text contains all required SOAP sections.
        
        Args:
            text: SOAP note text
            
        Returns:
            True if all required sections are present
        """
        return all(
            re.search(rf"(?i)\b{section}\b", text)
            for section in self.required_sections
        )
        
    def validate_batch(self, notes: List[str]) -> Tuple[List[str], List[str]]:
        """Split a batch of notes into valid and invalid ones.
        
        Args:
            notes: List of SOAP notes to validate
            
        Returns:
            Tuple of (valid_notes, invalid_notes)
        """
        valid_notes = []
        invalid_notes = []
        
        for note in notes:
            if self.has_all_sections(note):
                valid_notes.append(note)
            else:
                invalid_notes.append(note)
                
        return valid_notes, invalid_notes
        
    def save_validation_results(
        self,
        valid_notes: List[Dict],
        invalid_notes: List[Dict],
        valid_output: str,
        invalid_output: str
    ) -> None:
        """Save validation results to separate files.
        
        Args:
            valid_notes: List of valid note dictionaries
            invalid_notes: List of invalid note dictionaries
            valid_output: Path to save valid notes
            invalid_output: Path to save invalid notes
        """
        import json
        
        with open(valid_output, "w", encoding="utf-8") as f:
            for note in valid_notes:
                f.write(json.dumps(note) + "\n")
                
        with open(invalid_output, "w", encoding="utf-8") as f:
            for note in invalid_notes:
                f.write(json.dumps(note) + "\n")
                
        print("✅ Split results into:")
        print(f"- {valid_output} (complete SOAP notes)")
        print(f"- {invalid_output} (missing sections)") 