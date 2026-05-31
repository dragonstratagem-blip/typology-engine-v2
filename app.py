import streamlit as st
import re
import random

st.title("Typology Codification Engine")

# --- Logic ---
def apply_styles(letter, pol, mag, spol, smag, dof_val):
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = [f"font-family: {fonts[dof_val]};"]
    
    # Logic for Primary Polarity (Strictly + or -)
    if pol == "+": style.append("text-decoration: underline;")
    elif pol == "-": style.append("text-decoration: line-through;")
    
    # Magnitude (1-3)
    if mag == "3": style.append("font-weight: bold;")
    elif mag == "1": style.append("font-style: italic;")
    
    # Skill Polarity
    if spol == "+": style.append("vertical-align: super; font-size: smaller;")
    elif spol == "-": style.append("vertical-align: sub; font-size: smaller;")
    
    # Skill Magnitude (1-6)
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append(f"color: {colors[smag]};")
    return f"<span style='{' '.join(style)}'>{letter}</span>"

# --- UI Setup ---
dof = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], index=2)

cols = st.columns(4)
labels = ["PL", "PN", "PS", "PR"]
inputs = {}

for i, col in enumerate(cols):
    with col:
        st.subheader(labels[i])
        # Strict + or - only
        inputs[f"p{i}"] = st.selectbox(f"Pol {i+1}", ["+", "-"], index=0)
        inputs[f"m{i}"] = st.selectbox(f"Mag {i+1}", ["1", "2", "3"], index=0)
        inputs[f"sp{i}"] = st.selectbox(f"S-Pol {i+1}", [" ", "+", "-"], index=0)
        inputs[f"sm{i}"] = st.selectbox(f"S-Mag {i+1}", ["1", "2", "3", "4", "5", "6"], index=0)

# --- Randomization ---
if st.button("Randomize Values"):
    st.session_state.random_vals = [
        [random.randint(0,1), random.randint(0,2), random.randint(0,2), random.randint(0,5)] 
        for _ in range(4)
    ]
    st.rerun()

# --- Execution ---
if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, 
               "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    
    html_output = ""
    for i, label in enumerate(labels):
        letter = mapping[label][inputs[f"p{i}"]]
        html_output += apply_styles(letter, inputs[f"p{i}"], inputs[f"m{i}"], inputs[f"sp{i}"], inputs[f"sm{i}"], dof)
    
    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{html_output}</div>", unsafe_allow_html=True)