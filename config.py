import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Azure OpenAI and system settings."""
    
    def __init__(self):
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "").strip()
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").strip()
        self.model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini").strip()

def build_llm_config() -> dict:
    """Build LLM configuration from sidebar inputs and env vars"""
    # Initialize config from environment
    env_config = Config()
    
    # Get values from session state or environment
    model = st.session_state.get("model", env_config.model)
    api_key = st.session_state.get("api_key", env_config.api_key)
    base_url = st.session_state.get("base_url", env_config.endpoint)
    
    # Build config list entry
    config_entry = {
        "model": model,
        "api_key": api_key,
    }
    
    # For Azure OpenAI, we need to set api_type and other Azure-specific fields
    if base_url and ("azure" in base_url.lower() or "cognitiveservices" in base_url.lower()):
        config_entry["api_type"] = "azure"
        config_entry["azure_endpoint"] = base_url
        config_entry["api_version"] = env_config.api_version
        # For Azure, model is the deployment name
        config_entry["azure_deployment"] = model
    else:
        # For standard OpenAI
        if base_url:
            config_entry["base_url"] = base_url
    
    config = {
        "config_list": [config_entry],
        "timeout": st.session_state.get("timeout", 60),
        "seed": st.session_state.get("seed", 42),
        # Temperature removed - not supported in newer Azure OpenAI models
    }
    
    return config
