from dataclasses import dataclass
from typing import List, Dict
from autogen import ConversableAgent

@dataclass
class LineEval:
    """Evaluation data for a single comedian line"""
    speaker: str
    text: str
    score: float
    tags: List[str]
    comments: str
    round_idx: int

@dataclass
class ShowState:
    """Complete state of an improv show"""
    suggestion: str
    rounds: int
    order: List[ConversableAgent]
    critic: ConversableAgent
    transcript: List[Dict[str, str]]
    evaluations: List[LineEval]
    wrapped: bool
