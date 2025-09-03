import streamlit as st
import os
import traceback
import time
from config import build_llm_config
from orchestration import run_improv_streaming
from ui_components import display_transcript, display_scores, display_best_line, display_export
from models import ShowState, LineEval

# Streamlit UI
st.set_page_config(page_title="Improv Duo", page_icon="🎭", layout="wide")

# Initialize session state
if "show_state" not in st.session_state:
    st.session_state.show_state = None
if "streaming_state" not in st.session_state:
    st.session_state.streaming_state = None
if "is_running" not in st.session_state:
    st.session_state.is_running = False

# Sidebar settings
with st.sidebar:
    st.header("Settings")
    
    st.subheader("Model Configuration")
    model = st.text_input("Model", value=os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini"))
    api_key = st.text_input("API Key", value=os.getenv("AZURE_OPENAI_API_KEY", ""), type="password")
    base_url = st.text_input("Base URL (optional)", value=os.getenv("AZURE_OPENAI_ENDPOINT", ""))
    timeout = st.number_input("Timeout (seconds)", min_value=10, max_value=300, value=60)
    seed = st.number_input("Seed", value=42)
    
    st.subheader("Show Settings")
    rounds = st.slider("Rounds", 1, 8, 4)
    starter = st.selectbox("Who starts?", ["Random", "Cathy", "Joe"])
    
    # Save to session state
    st.session_state.model = model
    st.session_state.api_key = api_key
    st.session_state.base_url = base_url
    st.session_state.timeout = timeout
    st.session_state.seed = seed

# Main app
st.title("🎭 Improv Duo: Cathy & Joe (with a Critic)")

# Input section
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    suggestion = st.text_input("Audience suggestion", value="airport security")
with col2:
    run_button = st.button("Run Show", type="primary", use_container_width=True, disabled=st.session_state.is_running)
with col3:
    if st.button("Reset", use_container_width=True):
        st.session_state.show_state = None
        st.session_state.streaming_state = None
        st.session_state.is_running = False
        st.rerun()

# Run show with streaming
if run_button:
    if not st.session_state.get("api_key"):
        st.error("Please provide an API key in the sidebar.")
    else:
        st.session_state.is_running = True
        
        # Show current settings
        st.info(f"🎭 Starting {rounds} round{'s' if rounds > 1 else ''} with {starter} going first")
        
        # Create containers for streaming output
        transcript_container = st.container()
        scores_container = st.container()
        
        # Initialize streaming state
        st.session_state.streaming_state = ShowState(
            suggestion=suggestion,
            rounds=rounds,
            order=[],
            critic=None,
            transcript=[],
            evaluations=[],
            wrapped=False
        )
        
        try:
            llm_config = build_llm_config()
            
            # Callbacks for streaming
            def on_comedian_line(speaker: str, line: str, round_idx: int):
                """Handle new comedian line"""
                st.session_state.streaming_state.transcript.append({
                    "speaker": speaker,
                    "text": line
                })
                
                # Check if this comedian had feedback from previous round
                has_feedback = False
                if round_idx > 0 and st.session_state.streaming_state.evaluations:
                    # Look for this speaker's last evaluation
                    for eval in reversed(st.session_state.streaming_state.evaluations):
                        if eval.speaker.lower() == speaker.lower() and eval.round_idx < round_idx:
                            has_feedback = True
                            break
                
                # Update transcript display
                with transcript_container:
                    with st.chat_message(speaker):
                        if has_feedback:
                            st.caption("💭 *Considering critic feedback...*")
                        st.write(f"**{speaker}:** {line}")
                
                # Small delay for visual effect
                time.sleep(0.5)
            
            def on_critic_eval(eval: LineEval):
                """Handle new critic evaluation"""
                st.session_state.streaming_state.evaluations.append(eval)
                
                # Update scores display
                with scores_container:
                    st.write(f"🎯 **{eval.speaker.capitalize()}** scored {eval.score}/10 - {', '.join(eval.tags)}")
            
            # Run with streaming
            with st.spinner("🎭 Show in progress..."):
                st.session_state.show_state = run_improv_streaming(
                    suggestion, rounds, starter, llm_config,
                    on_comedian_line=on_comedian_line,
                    on_critic_eval=on_critic_eval
                )
            
            st.success("🎭 Show completed!")
            st.session_state.is_running = False
            
        except Exception as e:
            st.error(f"Error during show: {str(e)}")
            st.session_state.is_running = False
            
            # Show detailed error information
            with st.expander("Detailed Error Information"):
                st.code(traceback.format_exc())

# Display complete results after show
if st.session_state.show_state and not st.session_state.is_running:
    st.divider()
    st.subheader("📊 Complete Show Analysis")
    
    state = st.session_state.show_state
    
    # Display all components
    display_scores(state)
    display_best_line(state)
    display_export(state)
