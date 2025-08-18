import gradio as gr
from ..models.mistral_handler import MistralHandler
from ..evaluation.soap_validator import SOAPValidator


def create_app() -> gr.Interface:
    """Create and return the Gradio web interface.
    
    Returns:
        Gradio Interface object
    """
    model = MistralHandler()
    validator = SOAPValidator()
    
    def generate_and_validate_soap(transcript: str) -> tuple[str, str]:
        """Generate a SOAP note from a transcript and validate it.
        
        Args:
            transcript: The conversation transcript
            
        Returns:
            Tuple of (generated_soap, validation_info)
        """
        if not transcript.strip():
            return "Please provide a transcript.", "No validation performed."
            
        try:
            generated_soap = model.generate_soap(transcript)
            
            # Validate the generated SOAP note
            quality_checks = validator.validate_content_quality(generated_soap)
            validation_score = validator.get_validation_score(generated_soap)
            
            validation_info = f"""
Validation Results:
• Overall Score: {validation_score:.2f}/1.0
• Has all sections: {'✅' if quality_checks['has_all_sections'] else '❌'}
• Adequate length: {'✅' if quality_checks['min_length'] else '❌'}
• Not repetitive: {'✅' if quality_checks['not_repetitive'] else '❌'}
• Proper format: {'✅' if quality_checks['proper_format'] else '❌'}
            """
            
            return generated_soap, validation_info.strip()
            
        except Exception as e:
            return f"Error generating SOAP note: {str(e)}", "Validation failed due to generation error."
    
    return gr.Interface(
        fn=generate_and_validate_soap,
        inputs=gr.Textbox(lines=15, label="Paste transcript here", placeholder="Enter doctor-patient conversation transcript..."),
        outputs=[
            gr.Textbox(lines=20, label="Generated SOAP note"),
            gr.Textbox(lines=8, label="Validation Results")
        ],
        title="🩺 Clinical SOAP Note Generator",
        description="Paste a transcript of a doctor-patient conversation to generate a structured SOAP note using Mistral LLM.",
        examples=[
            ["Doctor: Good morning, how can I help you today?\nPatient: I've been having chest pain for the last two days..."],
        ]
    )

def main():
    """Launch the Gradio web interface."""
    app = create_app()
    app.launch()

if __name__ == "__main__":
    main() 