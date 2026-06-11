import streamlit as st
import random
import textwrap

# --- Game setup (simplified local generator) ---
def setup_game():
    victim_pool = ["Mr. Green", "Ms. Rose", "Dr. Patel", "Prof. Singh"]
    suspect_names = ["Alex", "Blake", "Casey"]

    victim = random.choice(victim_pool)
    suspects = suspect_names

    info = {
        "Alex": {"alibi": "I was in the garden watering plants.", "statement": "I saw someone near the back gate."},
        "Blake": {"alibi": "I was in the kitchen making tea.", "statement": "I heard a thud from the study."},
        "Casey": {"alibi": "I was reading in the study.", "statement": "I didn’t leave the study."}
    }

    crime_scene = {
        "location": "Study room",
        "description": f"The study where {victim} was found is dimly lit. Papers are scattered.",
        "clues": [
            "A muddy footprint by the window",
            "A torn piece of fabric with a blue thread",
            "A teacup with a lipstick mark"
        ]
    }

    murderer = random.choice(suspects)

    contradictions = {
        "A muddy footprint by the window": ("Alex", "Alex claimed to be in the garden, but footprint matches his boots.", 10),
        "A torn piece of fabric with a blue thread": ("Alex", "Alex mentioned a jacket with blue thread.", 12),
        "A teacup with a lipstick mark": ("Blake", "Blake said he never left the kitchen, but cup was in study.", 8)
    }

    return victim, suspects, info, crime_scene, contradictions, murderer

# --- Initialize session state ---
if "victim" not in st.session_state:
    st.session_state.victim, st.session_state.suspects, st.session_state.info, \
    st.session_state.crime_scene, st.session_state.contradictions, st.session_state.murderer = setup_game()
    st.session_state.clues_collected = []
    st.session_state.contradictions_found = []
    st.session_state.score = 0

# --- Sidebar ---
st.sidebar.title("🕵️ Detective Notebook")
st.sidebar.metric("Score", st.session_state.score)
if st.sidebar.button("Reset Case"):
    st.session_state.victim, st.session_state.suspects, st.session_state.info, \
    st.session_state.crime_scene, st.session_state.contradictions, st.session_state.murderer = setup_game()
    st.session_state.clues_collected = []
    st.session_state.contradictions_found = []
    st.session_state.score = 0

# --- Main UI ---
st.title("🔍 Murder Mystery Investigation")
st.subheader(f"Victim: {st.session_state.victim}")
st.write(st.session_state.crime_scene["description"])

# --- Clue display ---
with st.expander("Collected Clues"):
    if st.session_state.clues_collected:
        for clue in st.session_state.clues_collected:
            st.markdown(f"- {clue}")
    else:
        st.write("No clues collected yet.")

# --- Crime scene clues to collect ---
st.header("Crime Scene")
for clue in st.session_state.crime_scene["clues"]:
    if clue not in st.session_state.clues_collected:
        if st.button(f"Collect clue: {clue}"):
            st.session_state.clues_collected.append(clue)
            if clue in st.session_state.contradictions:
                suspect, explanation, pts = st.session_state.contradictions[clue]
                st.session_state.contradictions_found.append((clue, suspect, explanation, pts))
                st.session_state.score += pts
                st.success(f"Contradiction found! {suspect}: {explanation} (+{pts} pts)")
            else:
                st.info("Clue collected, no contradiction yet.")

# --- Suspect cards ---
st.header("Suspects")
cols = st.columns(len(st.session_state.suspects))
for i, s in enumerate(st.session_state.suspects):
    with cols[i]:
        st.subheader(s)
        st.write("**Alibi:**", st.session_state.info[s]["alibi"])
        st.write("**Statement:**", st.session_state.info[s]["statement"])
        if st.button(f"Accuse {s}"):
            if s == st.session_state.murderer:
                st.success(f"You accused correctly! {s} was the murderer. +25 pts")
                st.session_state.score += 25
            else:
                st.error(f"Wrong accusation! The murderer was {st.session_state.murderer}. -5 pts")
                st.session_state.score = max(0, st.session_state.score - 5)
