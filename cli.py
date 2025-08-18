#!/usr/bin/env python3
"""Command-line interface for Clinical SOAP Note Generator."""

import argparse
import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.pipeline import ClinicalPipeline, PipelineConfig
from src.web.app import main as web_main


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Clinical SOAP Note Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --root-dir . --pipeline           # Run full pipeline
  %(prog)s --root-dir . --training-data      # Generate training data
  %(prog)s --root-dir . --evaluate results.jsonl  # Evaluate results
  %(prog)s --web                             # Launch web interface
        """
    )
    
    # General options
    parser.add_argument("--root-dir", default=".", 
                       help="Root directory of the project (default: current directory)")
    parser.add_argument("--model", default="mistral",
                       help="Model name to use (default: mistral)")
    
    # Mode selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pipeline", action="store_true",
                      help="Run the full processing pipeline")
    group.add_argument("--training-data", action="store_true",
                      help="Generate training data in JSONL format")
    group.add_argument("--evaluate", metavar="FILE",
                      help="Evaluate generated notes from JSONL file")
    group.add_argument("--web", action="store_true",
                      help="Launch web interface")
    
    # Additional options
    parser.add_argument("--output", 
                       help="Output file path (for training data or evaluation)")
    
    args = parser.parse_args()
    
    if args.web:
        print("🚀 Launching web interface...")
        web_main()
        return
    
    # Create config and pipeline
    config = PipelineConfig.from_root_dir(args.root_dir)
    config.model_name = args.model
    pipeline = ClinicalPipeline(config)
    
    try:
        if args.pipeline:
            print("🚀 Running full processing pipeline...")
            paired_data = pipeline.run_full_pipeline()
            print(f"✅ Successfully processed {len(paired_data)} transcript-note pairs")
            
        elif args.training_data:
            print("📝 Generating training data...")
            output_file = pipeline.generate_training_data(args.output)
            print(f"✅ Training data saved to: {output_file}")
            
        elif args.evaluate:
            print(f"📊 Evaluating results from: {args.evaluate}")
            scores = pipeline.evaluate_generated_notes(args.evaluate, args.output)
            if scores:
                print("\n🎯 Evaluation completed successfully!")
            else:
                print("❌ No valid data found for evaluation")
                sys.exit(1)
                
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
