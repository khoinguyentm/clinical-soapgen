import gradio as gr
from ..models.mistral_handler import MistralHandler

def create_app() -> gr.Interface:
    """Create and return the Gradio web interface.
    
    Returns:
        Gradio Interface object
    """
    model = MistralHandler()
    
    def generate_soap(transcript: str) -> str:
        """Generate a SOAP note from a transcript.
        
        Args:
            transcript: The conversation transcript
            
        Returns:
            Generated SOAP note
        """
        return model.generate_soap(transcript)
    
    return gr.Interface(
        fn=generate_soap,
        inputs=gr.Textbox(lines=15, label="Paste transcript here"),
        outputs=gr.Textbox(lines=20, label="Generated SOAP note"),
        title="SOAP Note Generator",
        description="Paste a transcript of a doctor-patient conversation to generate a SOAP note using Mistral."
    )

def main():
    """Launch the Gradio web interface."""
    app = create_app()
    app.launch()

if __name__ == "__main__":
    main() 