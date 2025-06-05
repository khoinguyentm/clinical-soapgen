# 🩺 Clinical Note Generator from Doctor-Patient Conversations

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

## 🧮 Quick Stats

| Feature | Description |
|--------|-------------|
| Code cells | 12 |
| Markdown cells | 4 |
| Transcript files processed | 57+ |
| SOAP notes generated | Yes |
| Evaluation metric | ROUGE |
| Programming language | Python |
| Domain | Healthcare / Clinical NLP |

## 🗂️ Folder Structure

project/
├── audio/ # Original audio files
├── output/audio_utterances/ # Segmented utterances
├── transcripts/ # Processed transcripts (from TextGrid)
├── notes/ # Generated SOAP notes
├── scripts/ # Core processing and generation scripts
└── main.ipynb # End-to-end Jupyter workflow

bash
Copy
Edit

## 🚀 Getting Started

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/clinical-soap-pipeline.git
   cd clinical-soap-pipeline
2. Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt

3. Run the pipeline:
   Open main.ipynb and execute all cells in order.


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
