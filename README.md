# 🩺 Clinical SOAP Note Generator

This project implements a full clinical NLP pipeline that transforms audio-based medical consultations into structured SOAP (Subjective, Objective, Assessment, Plan) notes. It demonstrates the potential of AI-assisted documentation in real-world healthcare workflows using local language models.

## 📚 Project Summary

- 📦 **Dataset**: [Primock57](https://github.com/babylonhealth/primock57) – real doctor-patient conversations with aligned clinical notes.
- 🧠 **LLM-Driven**: Uses local Mistral model via [Ollama](https://ollama.com) to generate SOAP-format notes from transcripts.
- 📄 **TextGrid Parsing**: Extracts readable transcripts from Praat `.TextGrid` files.
- 🧪 **Evaluation**: Includes automated quality checks using ROUGE scoring.
- 🔍 **Focus Areas**:
  - ASR-error robustness
  - Note generation customization
  - Healthcare documentation support

## 🗂️ Project Structure

```
clinical-soapgen/
├── src/                      # Source code
│   ├── __init__.py          # Package initialization
│   ├── pipeline.py          # Core pipeline implementation
│   ├── evaluation/          # Evaluation tools
│   ├── models/             # Model implementations
│   ├── data/               # Data processing utilities
│   ├── config/             # Configuration management
│   └── web/                # Web interface
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── data/                    # Data directory
│   ├── audio/              # Original audio files
│   ├── transcripts/        # Processed transcripts
│   ├── notes/             # SOAP notes
│   └── output/            # Generated outputs
├── setup.py                # Package setup
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/clinical-soapgen.git
   cd clinical-soapgen
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package**:
   ```bash
   # Install in development mode with all dependencies
   pip install -e ".[dev]"
   ```

## 💻 Usage

### Command Line Interface

The package provides a command-line interface for running the full pipeline:

```bash
python -m clinical_soapgen.pipeline --root_dir /path/to/project --generate_training_data
```

### Python API

You can also use the package programmatically:

```python
from clinical_soapgen import ClinicalPipeline, PipelineConfig

# Initialize the pipeline
config = PipelineConfig.from_root_dir("/path/to/project")
pipeline = ClinicalPipeline(config)

# Run the full pipeline
paired_data = pipeline.run_full_pipeline()

# Generate training data
pipeline.generate_training_data()
```

### Jupyter Notebook

For interactive development and exploration, you can use the provided Jupyter notebook:

```bash
jupyter notebook main.ipynb
```

## 🧪 Development

1. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run tests**:
   ```bash
   pytest
   ```

3. **Format code**:
   ```bash
   black src tests
   ```

4. **Type checking**:
   ```bash
   mypy src
   ```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Citation

If you use this project in your research, please cite:

```bibtex
@software{clinical_soapgen,
  author = {Khoi Nguyen},
  title = {Clinical SOAP Note Generator},
  year = {2024},
  url = {https://github.com/your-username/clinical-soapgen}
}
```

🧠 Techniques Used
Parsing .TextGrid files into readable transcripts

Prompt-based generation using local LLMs (Mistral via Ollama)

Automatic note evaluation using ROUGE scores

File filtering and pipeline automation with Python

🏥 Why This Matters
Manual clinical documentation is time-consuming and error-prone. This project demonstrates how AI can:

Reduce physician burden

Improve note accuracy and consistency

Act as a prototype for real-time clinical documentation tools
