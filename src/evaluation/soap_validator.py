import re
from typing import Dict, List, Tuple

from ..config import settings

class SOAPValidator:
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
        
    def extract_sections(self, soap_text: str) -> Dict[str, str]:
        """Extract individual SOAP sections from text."""
        sections = {}
        current_section = None
        current_content = []
        
        for line in soap_text.splitlines():
            line = line.strip()
            
            # Check if line starts a new section
            for section in self.required_sections:
                if line.lower().startswith(section.lower()):
                    # Save previous section if exists
                    if current_section:
                        sections[current_section] = " ".join(current_content)
                    
                    # Start new section
                    current_section = section
                    current_content = [line]
                    break
            else:
                # Continue current section
                if current_section and line:
                    current_content.append(line)
        
        # Save final section
        if current_section:
            sections[current_section] = " ".join(current_content)
            
        return sections
        
    def validate_content_quality(self, soap_text: str) -> Dict[str, bool]:
        """Perform basic content quality checks."""
        checks = {
            "has_all_sections": self.has_all_sections(soap_text),
            "min_length": len(soap_text.strip()) > 50,
            "not_repetitive": self._check_repetitiveness(soap_text),
            "proper_format": self._check_format(soap_text)
        }
        return checks
        
    def get_validation_score(self, soap_text: str) -> float:
        """Get overall validation score (0.0 to 1.0)."""
        checks = self.validate_content_quality(soap_text)
        return sum(checks.values()) / len(checks)
        
    def _check_repetitiveness(self, text: str, threshold: float = 0.7) -> bool:
        """Check if text is overly repetitive."""
        words = text.lower().split()
        if len(words) < 10:
            return True
            
        unique_words = set(words)
        repetition_ratio = len(unique_words) / len(words)
        return repetition_ratio > threshold
        
    def _check_format(self, text: str) -> bool:
        """Check basic formatting requirements."""
        # Check for section headers
        has_headers = any(
            section.lower() in text.lower() 
            for section in self.required_sections
        )
        
        # Check for reasonable length per section
        sections = self.extract_sections(text)
        adequate_length = all(
            len(content.strip()) > 10 
            for content in sections.values()
        ) if sections else False
        
        return has_headers and adequate_length 