import streamlit as st
import pandas as pd
import json
from models import ShowState, LineEval
from utils import evaluations_df, average_scores, best_line

def display_transcript(state: ShowState):
    """Display the show transcript"""
    st.subheader("📝 Transcript")
    for msg in state.transcript:
        with st.chat_message(msg["speaker"]):
            st.write(f"**{msg['speaker']}:** {msg['text']}")

def display_scores(state: ShowState):
    """Display scores table and charts"""
    st.subheader("📊 Scores")
    if state.evaluations:
        df = evaluations_df(state.evaluations)
        st.dataframe(df, use_container_width=True)
        
        # Average scores chart
        st.subheader("📈 Average Scores")
        avg_scores = average_scores(state.evaluations)
        chart_df = pd.DataFrame(list(avg_scores.items()), columns=["Speaker", "Average Score"])
        st.bar_chart(chart_df.set_index("Speaker"))

def display_best_line(state: ShowState):
    """Display the best line"""
    st.subheader("🏆 Best Line")
    best = best_line(state.evaluations)
    if best:
        st.success(f"**{best.speaker.capitalize()}** (Score: {best.score})")
        st.write(f"*\"{best.text}\"*")
        if best.tags:
            st.write(f"Tags: {', '.join(best.tags)}")
        if best.comments:
            st.write(f"Judge's note: {best.comments}")

def display_export(state: ShowState):
    """Display export options"""
    st.subheader("💾 Export")
    export_data = {
        "suggestion": state.suggestion,
        "rounds": state.rounds,
        "wrapped": state.wrapped,
        "transcript": state.transcript,
        "evaluations": [
            {
                "speaker": e.speaker,
                "text": e.text,
                "score": e.score,
                "tags": e.tags,
                "comments": e.comments,
                "round": e.round_idx + 1
            }
            for e in state.evaluations
        ],
        "averages": average_scores(state.evaluations)
    }
    
    st.download_button(
        label="Download JSON",
        data=json.dumps(export_data, indent=2),
        file_name=f"improv_show_{state.suggestion.replace(' ', '_')}.json",
        mime="application/json"
    )

def display_score_update(eval: LineEval):
    """Display a single score update in a compact format"""
    score_emoji = "🔥" if eval.score >= 8 else "👍" if eval.score >= 6 else "🤔"
    st.write(f"{score_emoji} **{eval.speaker.capitalize()}** scored {eval.score}/10")
    if eval.tags:
        st.caption(f"Tags: {', '.join(eval.tags)}")
    if eval.comments:
        st.caption(f"💭 {eval.comments}")

def display_transcript_streaming(transcript_entry: dict):
    """Display a single transcript entry for streaming"""
    with st.chat_message(transcript_entry["speaker"]):
        st.write(f"**{transcript_entry['speaker']}:** {transcript_entry['text']}")
