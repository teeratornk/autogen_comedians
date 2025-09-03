import json
import random
import logging
from typing import Optional, Tuple, Callable
from autogen import ConversableAgent
from models import LineEval, ShowState
from agents import make_comedian, make_critic
from utils import average_scores

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def critic_judge_line(critic: ConversableAgent, speaker: str, line: str, suggestion: str, round_idx: int) -> LineEval:
    """Have critic evaluate a comedian's line"""
    prompt = f"""Suggestion: "{suggestion}"
Speaker: {speaker}
Line: "{line}"

Evaluate this line and return JSON only."""
    
    try:
        logger.debug(f"Critic evaluating line from {speaker}")
        response = critic.generate_reply(messages=[{"role": "user", "content": prompt}])
        logger.debug(f"Critic response: {response}")
        
        result = json.loads(response)
        
        return LineEval(
            speaker=result.get("speaker", speaker).lower(),
            text=line,
            score=float(result.get("score", 0)),
            tags=result.get("tags", []),
            comments=result.get("comments", ""),
            round_idx=round_idx
        )
    except Exception as e:
        logger.error(f"Error in critic evaluation: {str(e)}")
        # Fallback on parse failure
        return LineEval(
            speaker=speaker.lower(),
            text=line,
            score=0.0,
            tags=["parse-failed"],
            comments="Unable to evaluate",
            round_idx=round_idx
        )

def comedian_turn(comedian: ConversableAgent, state: ShowState, prior_partner_line: Optional[str], 
                  round_idx: int, last_feedback: Optional[LineEval] = None) -> Tuple[str, bool]:
    """Execute a comedian's turn"""
    suggestion = state.suggestion
    
    if prior_partner_line:
        prompt = f"""Improv scene. Suggestion: {suggestion}. Round {round_idx + 1} of {state.rounds}. Keep ≤2 sentences. Build on scene; don't repeat.
Your partner just said: "{prior_partner_line}"
Respond with your next line."""
        
        # Add critic feedback if available
        if last_feedback and last_feedback.speaker.lower() == comedian.name.lower():
            prompt += f"\n\nYour last line scored {last_feedback.score}/10. Critic noted: {last_feedback.comments}"
    else:
        prompt = f"""Improv scene. Suggestion: {suggestion}. Round {round_idx + 1} of {state.rounds}. Keep ≤2 sentences.
Open the scene with a strong first line."""
    
    try:
        logger.debug(f"Comedian {comedian.name} generating response")
        logger.debug(f"Prompt: {prompt}")
        
        # Generate reply with proper message format
        messages = [{"role": "user", "content": prompt}]
        response = comedian.generate_reply(messages=messages)
        
        logger.debug(f"Comedian response: {response}")
        
        # Check for termination
        termination_phrases = ["I gotta go", "Goodbye"]
        did_terminate = any(phrase.lower() in response.lower() for phrase in termination_phrases)
        
        return response, did_terminate
    except Exception as e:
        logger.error(f"Error in comedian turn: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        raise

def run_improv_streaming(suggestion: str, rounds: int, starter_choice: str, llm_config: dict, 
                        on_comedian_line: Callable = None, on_critic_eval: Callable = None) -> ShowState:
    """Run the full improv show with streaming callbacks"""
    try:
        logger.info(f"Starting improv show with suggestion: {suggestion}")
        logger.debug(f"LLM Config: {llm_config}")
        logger.info(f"Rounds: {rounds}")
        
        # Create agents
        cathy = make_comedian("Cathy", llm_config)
        joe = make_comedian("Joe", llm_config)
        critic = make_critic(llm_config)
        
        # Determine order
        if starter_choice == "Random":
            order = [cathy, joe] if random.random() < 0.5 else [joe, cathy]
        elif starter_choice == "Cathy":
            order = [cathy, joe]
        else:
            order = [joe, cathy]
        
        state = ShowState(
            suggestion=suggestion,
            rounds=rounds,
            order=order,
            critic=critic,
            transcript=[],
            evaluations=[],
            wrapped=False
        )
        
        # Track last feedback for each comedian
        last_feedback = {"Cathy": None, "Joe": None}
        
        # Run rounds
        for round_idx in range(rounds):
            # Speaker A turn
            speaker_a = order[0]
            prior_line = state.transcript[-1]["text"] if len(state.transcript) > 1 else None
            
            line_a, did_terminate = comedian_turn(speaker_a, state, prior_line, round_idx, 
                                                  last_feedback.get(speaker_a.name))
            state.transcript.append({"speaker": speaker_a.name, "text": line_a})
            
            # Callback for streaming
            if on_comedian_line:
                on_comedian_line(speaker_a.name, line_a, round_idx)
            
            # Evaluate
            eval_a = critic_judge_line(critic, speaker_a.name, line_a, suggestion, round_idx)
            state.evaluations.append(eval_a)
            last_feedback[speaker_a.name] = eval_a  # Store feedback
            
            # Callback for critic evaluation
            if on_critic_eval:
                on_critic_eval(eval_a)
            
            if did_terminate:
                state.wrapped = True
                break
            
            # Speaker B turn
            speaker_b = order[1]
            line_b, did_terminate = comedian_turn(speaker_b, state, line_a, round_idx,
                                                  last_feedback.get(speaker_b.name))
            state.transcript.append({"speaker": speaker_b.name, "text": line_b})
            
            # Callback for streaming
            if on_comedian_line:
                on_comedian_line(speaker_b.name, line_b, round_idx)
            
            # Evaluate
            eval_b = critic_judge_line(critic, speaker_b.name, line_b, suggestion, round_idx)
            state.evaluations.append(eval_b)
            last_feedback[speaker_b.name] = eval_b  # Store feedback
            
            # Callback for critic evaluation
            if on_critic_eval:
                on_critic_eval(eval_b)
            
            if did_terminate:
                state.wrapped = True
                break
        
        return state
    except Exception as e:
        logger.error(f"Error in run_improv: {str(e)}")
        raise

# Keep the original function for backward compatibility
def run_improv(suggestion: str, rounds: int, starter_choice: str, llm_config: dict) -> ShowState:
    """Run the full improv show (non-streaming version)"""
    return run_improv_streaming(suggestion, rounds, starter_choice, llm_config, 
                               on_comedian_line=None, on_critic_eval=None)
