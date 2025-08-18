"""Core pipeline for processing clinical conversations and generating SOAP notes."""

import json
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from .config.settings import (
    AUDIO_DIR,
    TRANSCRIPT_DIR, 
    NOTES_DIR,
    JOINED_TRANSCRIPTS_DIR,
    TRAINING_DATA_DIR,
    REQUIRED_SECTIONS,
    PROMPT_TEMPLATE
)
from .models.mistral_handler import MistralHandler
from .evaluation.rouge_evaluator import RougeEvaluator
from .data.textgrid_processor import convert_textgrid_to_transcripts, extract_utterances


class PipelineConfig:
    """Configuration class for the Clinical Pipeline."""
    
    def __init__(
        self,
        audio_dir: Path,
        transcript_dir: Path, 
        notes_dir: Path,
        output_dir: Path,
        model_name: str = "mistral"
    ):
        self.audio_dir = Path(audio_dir)
        self.transcript_dir = Path(transcript_dir)
        self.notes_dir = Path(notes_dir)
        self.output_dir = Path(output_dir)
        self.model_name = model_name
        
        # Create subdirectories
        self.joined_transcripts_dir = self.output_dir / "joined_transcripts"
        self.training_data_dir = self.output_dir / "training_data"
        
        # Ensure directories exist
        for dir_path in [
            self.output_dir,
            self.joined_transcripts_dir, 
            self.training_data_dir
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_root_dir(cls, root_dir: str | Path) -> "PipelineConfig":
        """Create config from root directory path."""
        root = Path(root_dir)
        return cls(
            audio_dir=root / "audio",
            transcript_dir=root / "transcripts", 
            notes_dir=root / "notes",
            output_dir=root / "output"
        )


class ClinicalPipeline:
    """Main pipeline for processing clinical conversations."""
    
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.model = MistralHandler(config.model_name)
        self.evaluator = RougeEvaluator()
        
    def convert_textgrids(self) -> None:
        """Convert TextGrid files to readable transcripts."""
        print("Converting TextGrid files to transcripts...")
        subprocess.run([
            "python", "scripts/textgrid_to_transcript.py",
            f"--transcript_path={self.config.transcript_dir}",
            f"--output_path={self.config.joined_transcripts_dir}"
        ])
        
    def extract_audio_utterances(self) -> None:
        """Extract individual utterances from audio and transcripts."""
        print("Extracting utterances from transcripts...")
        subprocess.run([
            "python", "scripts/extract_utterances.py",
            f"--audio_path={self.config.audio_dir}",
            f"--transcript_path={self.config.transcript_dir}",
            f"--output_path={self.config.output_dir}"
        ])
    
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
        
        transcript_files = sorted(self.config.joined_transcripts_dir.glob("*.txt"))
        note_files = sorted(self.config.notes_dir.glob("*.txt"))

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
        
    def generate_training_data(self, output_file: Optional[str] = None) -> str:
        """Generate training data in JSONL format.
        
        Args:
            output_file: Output file path (defaults to training_data/mistral_prompt_data.jsonl)
            
        Returns:
            Path to the generated training data file
        """
        if output_file is None:
            output_file = self.config.training_data_dir / "mistral_prompt_data.jsonl"
        else:
            output_file = Path(output_file)
            
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with output_file.open("w", encoding="utf-8") as outfile:
            for transcript_file in sorted(self.config.joined_transcripts_dir.glob("*.txt")):
                base_name = transcript_file.stem
                note_file = self.config.notes_dir / f"{base_name}.txt"

                if not note_file.exists():
                    print(f"❌ Missing SOAP note for {base_name}")
                    continue

                transcript = transcript_file.read_text(encoding="utf-8").strip()
                note = note_file.read_text(encoding="utf-8").strip()

                prompt = PROMPT_TEMPLATE.format(transcript=transcript)

                entry = {
                    "prompt": prompt,
                    "response": note,
                    "transcript_file": str(transcript_file),
                    "note_file": str(note_file)
                }

                outfile.write(json.dumps(entry) + "\n")

        print(f"✅ Saved formatted training data to {output_file}")
        return str(output_file)
        
    def evaluate_generated_notes(
        self, 
        generated_file: str,
        output_file: Optional[str] = None
    ) -> Dict[str, float]:
        """Evaluate generated SOAP notes using ROUGE metrics.
        
        Args:
            generated_file: Path to file with generated notes
            output_file: Optional path to save evaluation results
            
        Returns:
            Dictionary of average ROUGE scores
        """
        references = []
        generated = []
        
        with open(generated_file, "r", encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                if item.get("generated") and item.get("reference"):
                    generated.append(item["generated"])
                    references.append(item["reference"])
        
        if not generated:
            print("❌ No valid generated/reference pairs found")
            return {}
            
        scores = self.evaluator.evaluate_batch(references, generated)
        
        print(f"\n📊 ROUGE Evaluation Results ({len(generated)} samples):")
        for metric, score in scores.items():
            print(f"{metric.upper()}: {score:.4f}")
            
        if output_file:
            with open(output_file, "w") as f:
                json.dump(scores, f, indent=2)
                
        return scores
        
    def filter_complete_soap_notes(
        self,
        input_file: str,
        valid_output: Optional[str] = None,
        incomplete_output: Optional[str] = None
    ) -> Tuple[str, str]:
        """Filter notes based on whether they contain all SOAP sections.
        
        Args:
            input_file: Input JSONL file with generated notes
            valid_output: Output file for complete notes
            incomplete_output: Output file for incomplete notes
            
        Returns:
            Tuple of (valid_file_path, incomplete_file_path)
        """
        if valid_output is None:
            valid_output = self.config.training_data_dir / "valid_soap_notes.jsonl"
        if incomplete_output is None:
            incomplete_output = self.config.training_data_dir / "incomplete_soap_notes.jsonl"
            
        def has_all_sections(text: str) -> bool:
            return all(
                re.search(rf"(?i)\b{section}\b", text) 
                for section in REQUIRED_SECTIONS
            )

        valid_count = 0
        incomplete_count = 0
        
        with open(input_file, "r") as infile, \
             open(valid_output, "w") as valid_out, \
             open(incomplete_output, "w") as incomplete_out:

            for line in infile:
                item = json.loads(line)
                generated = item.get("generated", "")

                if has_all_sections(generated):
                    valid_out.write(line)
                    valid_count += 1
                else:
                    incomplete_out.write(line)
                    incomplete_count += 1

        print(f"✅ Filtered {valid_count} complete and {incomplete_count} incomplete SOAP notes")
        return str(valid_output), str(incomplete_output)
        
    def run_full_pipeline(self) -> List[Tuple[str, Dict[str, str]]]:
        """Run the complete pipeline from TextGrid to paired data.
        
        Returns:
            List of (transcript, soap_sections) tuples
        """
        print("🚀 Starting full Clinical SOAP pipeline...")
        
        # Step 1: Convert TextGrid files
        self.convert_textgrids()
        
        # Step 2: Extract utterances 
        self.extract_audio_utterances()
        
        # Step 3: Pair transcripts with notes
        paired_data = self.pair_transcripts_and_notes()
        
        print(f"✅ Pipeline complete! Generated {len(paired_data)} transcript-note pairs.")
        return paired_data


def main():
    """Command-line interface for the pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Clinical SOAP Note Generation Pipeline")
    parser.add_argument("--root_dir", required=True, help="Root directory of the project")
    parser.add_argument("--generate_training_data", action="store_true", 
                       help="Generate training data in JSONL format")
    parser.add_argument("--evaluate", help="Evaluate generated notes file")
    
    args = parser.parse_args()
    
    config = PipelineConfig.from_root_dir(args.root_dir)
    pipeline = ClinicalPipeline(config)
    
    if args.generate_training_data:
        pipeline.generate_training_data()
    elif args.evaluate:
        pipeline.evaluate_generated_notes(args.evaluate)
    else:
        pipeline.run_full_pipeline()


if __name__ == "__main__":
    main()
