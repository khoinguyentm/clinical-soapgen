from typing import Dict, List
from rouge_score import rouge_scorer

class RougeEvaluator:
    """Evaluator for computing ROUGE scores between reference and generated text."""
    
    def __init__(self, metrics: List[str] = ['rouge1', 'rouge2', 'rougeL']):
        self.scorer = rouge_scorer.RougeScorer(metrics, use_stemmer=True)
        self.metrics = metrics
        
    def evaluate_single(self, reference: str, generated: str) -> Dict[str, float]:
        """Evaluate a single pair of reference and generated text.
        
        Args:
            reference: Reference text
            generated: Generated text
            
        Returns:
            Dictionary of metric scores
        """
        scores = self.scorer.score(reference, generated)
        return {metric: scores[metric].fmeasure for metric in self.metrics}
        
    def evaluate_batch(self, references: List[str], generated: List[str]) -> Dict[str, float]:
        """Evaluate multiple pairs of reference and generated text.
        
        Args:
            references: List of reference texts
            generated: List of generated texts
            
        Returns:
            Dictionary of average metric scores
        """
        if len(references) != len(generated):
            raise ValueError("References and generated lists must have same length")
            
        all_scores = {metric: [] for metric in self.metrics}
        
        for ref, gen in zip(references, generated):
            scores = self.evaluate_single(ref, gen)
            for metric, score in scores.items():
                all_scores[metric].append(score)
                
        # Calculate averages
        avg_scores = {
            metric: sum(scores) / len(scores)
            for metric, scores in all_scores.items()
        }
        
        return avg_scores 