import pandas as pd
from typing import List, Dict, Optional
from models import LineEval

def average_scores(evals: List[LineEval]) -> Dict[str, float]:
    """Calculate average scores by speaker"""
    scores = {}
    counts = {}
    
    for eval in evals:
        speaker = eval.speaker.capitalize()
        if speaker not in scores:
            scores[speaker] = 0
            counts[speaker] = 0
        scores[speaker] += eval.score
        counts[speaker] += 1
    
    return {speaker: scores[speaker] / counts[speaker] for speaker in scores if counts[speaker] > 0}

def best_line(evals: List[LineEval]) -> Optional[LineEval]:
    """Find the highest scoring line"""
    if not evals:
        return None
    return max(evals, key=lambda e: e.score)

def evaluations_df(evals: List[LineEval]) -> pd.DataFrame:
    """Convert evaluations to DataFrame"""
    data = []
    for eval in evals:
        data.append({
            "round": eval.round_idx + 1,
            "speaker": eval.speaker.capitalize(),
            "score": eval.score,
            "tags": ", ".join(eval.tags),
            "comments": eval.comments,
            "text": eval.text
        })
    return pd.DataFrame(data)
