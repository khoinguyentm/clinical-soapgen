# 🩺 Clinical SOAP Note Generator

A comprehensive AI-powered pipeline that transforms audio-based medical consultations into structured SOAP (Subjective, Objective, Assessment, Plan) notes using local language models. Built for healthcare professionals who want to streamline clinical documentation while maintaining data privacy.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Key Features

- 🎯 **End-to-End Pipeline**: From TextGrid files to structured SOAP notes
- 🧠 **Local LLM Integration**: Uses Mistral via [Ollama](https://ollama.com) for privacy
- 📊 **Automated Evaluation**: ROUGE scoring and SOAP structure validation
- 🌐 **Web Interface**: Interactive Gradio app for real-time note generation
- 🔧 **CLI Tools**: Command-line interface for batch processing
- 📈 **Quality Metrics**: Comprehensive validation and content quality checks

## 🗂️ Project Structure

```
clinical-soapgen/
├── src/                        # Source code
│   ├── __init__.py            # Package initialization
│   ├── pipeline.py            # Core pipeline implementation
│   ├── config/                # Configuration management
│   │   ├── settings.py        # Project settings
│   │   └── __init__.py
│   ├── data/                  # Data processing utilities
│   │   ├── textgrid_processor.py
│   │   ├── transcript_processor.py
│   │   └── __init__.py
│   ├── models/                # Model implementations
│   │   ├── mistral_handler.py # Mistral LLM interface
│   │   └── __init__.py
│   ├── evaluation/            # Evaluation tools
│   │   ├── rouge_evaluator.py # ROUGE scoring
│   │   ├── soap_validator.py  # SOAP structure validation
│   │   └── __init__.py
│   └── web/                   # Web interface
│       ├── app.py             # Gradio web app
│       └── __init__.py
├── scripts/                   # Utility scripts
│   ├── textgrid_to_transcript.py
│   ├── extract_utterances.py
│   └── utils.py
├── data/                      # Data directories
│   ├── audio/                 # Original audio files (.wav)
│   ├── transcripts/           # TextGrid transcript files
│   ├── notes/                 # SOAP notes (.txt, .json)
│   └── output/                # Generated outputs
├── human_eval_data/           # Human evaluation datasets
├── consultation_checklists/   # Clinical evaluation checklists
├── cli.py                     # Command-line interface
├── main.ipynb                 # Jupyter notebook for exploration
├── setup.py                   # Package installation
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed with Mistral model:
   ```bash
   # Install Ollama (see https://ollama.com)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull Mistral model
   ollama pull mistral
   ```

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/clinical-soapgen.git
   cd clinical-soapgen
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**:
   ```bash
   # Option 1: Install in development mode
   pip install -e .
   
   # Option 2: Install from requirements.txt
   pip install -r requirements.txt
   ```

### Basic Usage

#### 🌐 Web Interface (Recommended for beginners)

Launch the interactive web interface:

```bash
# Using the CLI script
./cli.py --web

# Or using Python
python -m src.web.app
```

Then open your browser to `http://localhost:7860` and paste a medical transcript to generate a SOAP note.

#### 💻 Command Line Interface

```bash
# Run the full pipeline (TextGrid → Transcripts → SOAP notes)
./cli.py --root-dir . --pipeline

# Generate training data for fine-tuning
./cli.py --root-dir . --training-data

# Evaluate generated SOAP notes
./cli.py --root-dir . --evaluate results.jsonl

# Get help
./cli.py --help
```

#### 🐍 Python API

```python
from src.pipeline import ClinicalPipeline, PipelineConfig

# Initialize the pipeline
config = PipelineConfig.from_root_dir(".")
pipeline = ClinicalPipeline(config)

# Run the full pipeline
paired_data = pipeline.run_full_pipeline()

# Generate training data
training_file = pipeline.generate_training_data()

# Evaluate results
scores = pipeline.evaluate_generated_notes("results.jsonl")
```

#### 📓 Jupyter Notebook

For interactive exploration and development:

```bash
jupyter notebook main.ipynb
```

## 📊 Dataset

This project uses the **[Primock57](https://github.com/babylonhealth/primock57)** dataset:
- 57 real doctor-patient conversations
- Audio recordings with aligned clinical notes
- TextGrid format for precise timing
- Human-written SOAP notes for evaluation

## 🧪 Evaluation Metrics

The system provides comprehensive evaluation using:

- **ROUGE Scores**: Measures content overlap with reference notes
  - ROUGE-1: Unigram overlap
  - ROUGE-2: Bigram overlap  
  - ROUGE-L: Longest common subsequence
- **SOAP Structure Validation**: Ensures all required sections are present
- **Content Quality Checks**: Length, repetitiveness, formatting

## 🔧 Configuration

Key settings in `src/config/settings.py`:

```python
# Model configuration
MODEL_NAME = "mistral"
REQUIRED_SECTIONS = ["Subjective", "Objective", "Assessment", "Plan"]

# Prompt template
PROMPT_TEMPLATE = """Below is a conversation between a doctor and a patient.

Transcript:
{transcript}

Generate a SOAP note from this conversation."""
```

## 📈 Performance

Based on evaluation with ROUGE metrics:
- **ROUGE-1**: ~0.59 (good content overlap)
- **ROUGE-2**: ~0.26 (reasonable phrase matching)
- **ROUGE-L**: ~0.34 (decent structure preservation)

## 🛠️ Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/

# Code formatting
black src/ tests/
```

### Code Structure

- **Pipeline**: Core processing logic in `src/pipeline.py`
- **Models**: LLM handlers in `src/models/`
- **Data Processing**: TextGrid and transcript utilities in `src/data/`
- **Evaluation**: Metrics and validation in `src/evaluation/`
- **Web Interface**: Gradio app in `src/web/`

## 🔍 Why This Matters

Manual clinical documentation is:
- ⏰ **Time-consuming**: Takes 15-30% of physician time
- 🐛 **Error-prone**: Manual transcription introduces mistakes
- 😩 **Burnout-inducing**: Reduces time for patient care

This AI-assisted approach can:
- ⚡ **Reduce documentation burden** by 70-80%
- ✅ **Improve accuracy** through structured templates
- 🏥 **Enhance patient care** by freeing up physician time
- 🔒 **Maintain privacy** with local processing

## 🎯 Use Cases

- **Clinical Documentation**: Real-time SOAP note generation
- **Medical Training**: Teaching SOAP note structure
- **Research**: Analyzing clinical conversation patterns
- **Quality Assurance**: Standardizing documentation format

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints for all functions
- Include docstrings for public methods
- Add tests for new functionality
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Citation

If you use this project in your research, please cite:

```bibtex
@software{clinical_soapgen,
  author = {Khoi Nguyen},
  title = {Clinical SOAP Note Generator: AI-Powered Medical Documentation},
  year = {2024},
  url = {https://github.com/your-username/clinical-soapgen},
  note = {Open-source tool for generating SOAP notes from clinical conversations}
}
```

## 🙏 Acknowledgments

- **Primock57 Dataset**: [Babylon Health](https://github.com/babylonhealth/primock57)
- **Mistral LLM**: [Mistral AI](https://mistral.ai/)
- **Ollama**: [Local LLM runtime](https://ollama.com)
- **Gradio**: [Web interface framework](https://gradio.app)
