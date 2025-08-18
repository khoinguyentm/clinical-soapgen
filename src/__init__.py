"""Clinical SOAP Note Generator Package.

A tool for generating SOAP notes from clinical conversations using Mistral LLM.
"""

__version__ = "0.1.0"
__author__ = "Khoi Nguyen"

from .pipeline import ClinicalPipeline, PipelineConfig
from .models.mistral_handler import MistralHandler
from .evaluation.rouge_evaluator import RougeEvaluator

__all__ = [
    "ClinicalPipeline",
    "PipelineConfig", 
    "MistralHandler",
    "RougeEvaluator",
]
