from autogen import ConversableAgent
import logging

logger = logging.getLogger(__name__)

def make_comedian(name: str, llm_config: dict) -> ConversableAgent:
    """Create a comedian agent"""
    system_message = f"""Your name is {name} and you are a quick-witted, kind stand-up comedian.
You are performing an improv scene based on the audience suggestion.
Rules:
- Keep each line to 2 sentences or less
- Always tie your response to the original suggestion
- Be playful but keep it safe and clean
- When asked to wrap up, end with "I gotta go"
"""
    
    def termination_predicate(messages):
        if messages and isinstance(messages, list) and len(messages) > 0:
            last_msg = messages[-1]
            if isinstance(last_msg, dict):
                content = last_msg.get("content", "")
            else:
                content = str(last_msg)
            termination_phrases = ["I gotta go", "Goodbye"]
            return any(phrase.lower() in content.lower() for phrase in termination_phrases)
        return False
    
    try:
        logger.debug(f"Creating comedian agent: {name}")
        logger.debug(f"LLM config for {name}: {llm_config}")
        
        agent = ConversableAgent(
            name=name,
            system_message=system_message,
            llm_config=llm_config,
            is_termination_msg=termination_predicate,
            human_input_mode="NEVER"
        )
        
        logger.debug(f"Successfully created {name}")
        return agent
    except Exception as e:
        logger.error(f"Error creating comedian {name}: {str(e)}")
        raise

def make_critic(llm_config: dict) -> ConversableAgent:
    """Create a critic agent with low temperature"""
    system_message = """You are a comedy judge. Evaluate ONLY the last comedian line shown.
Use this rubric (0-10 total):
- Relevance to suggestion (0-2)
- Setup to punch coherence (0-3)
- Originality (0-3)
- Punch impact (0-2)

Output strictly JSON, no extra text:
{"speaker":"<name>","score":<0-10>,"tags":["..."],"comments":"..."}
"""
    
    # For newer Azure OpenAI models, temperature is not supported
    # Just use the same config as comedians
    critic_config = llm_config.copy()
    
    try:
        logger.debug("Creating critic agent")
        logger.debug(f"Critic config: {critic_config}")
        
        agent = ConversableAgent(
            name="Critic",
            system_message=system_message,
            llm_config=critic_config,
            human_input_mode="NEVER"
        )
        
        logger.debug("Successfully created critic")
        return agent
    except Exception as e:
        logger.error(f"Error creating critic: {str(e)}")
        raise
