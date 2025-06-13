import subprocess
from typing import Optional

from ..config import settings

class MistralHandler:
    """Handler for interacting with the Mistral model via Ollama."""
    
    def __init__(self, model_name: str = settings.MODEL_NAME):
        self.model_name = model_name
        
    def generate_soap(self, transcript: str) -> str:
        """Generate a SOAP note from a transcript.
        
        Args:
            transcript: The conversation transcript
            
        Returns:
            Generated SOAP note
        """
        prompt = settings.PROMPT_TEMPLATE.format(transcript=transcript)
        
        result = subprocess.run(
            ["ollama", "run", self.model_name],
            input=prompt,
            capture_output=True,
            text=True
        )
        
        return result.stdout.strip()
        
    def batch_generate(self, transcripts: list[str], output_file: str) -> None:
        """Generate SOAP notes for multiple transcripts and save to file.
        
        Args:
            transcripts: List of transcripts to process
            output_file: Path to save the generated notes
        """
        import json
        
        with open(output_file, "w", encoding="utf-8") as f:
            for i, transcript in enumerate(transcripts, 1):
                print(f"🧠 Generating SOAP for example {i}...")
                generated = self.generate_soap(transcript)
                
                entry = {
                    "id": i,
                    "transcript": transcript,
                    "generated": generated
                }
                
                f.write(json.dumps(entry) + "\n")
                
        print(f"✅ Saved all generated notes to {output_file}") 