import streamlit as st
import random

st.title("Typology Codification Engine")

# --- Logic ---
def apply_styles(letter, pol, mag_pol, mag_val, spol, smag, dof_val):
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = [f"font-family: {fonts[dof_val]};"]
    
    # Polarity
    if pol == "+": style.append("text-decoration: underline;")
    elif pol == "-": style.append("text-decoration: line-through;")
    
    # Magnitude Polarity (using mag_pol) and Magnitude Value (using mag_val)
    if mag_pol == "+": style.append("font-weight: bold;")
    elif mag_pol == "-": style.append("font-style: italic;")
    
    # Skill Polarity
    if spol == "+": style.append("vertical-align: super; font-size: smaller;")
    elif spol == "-": style.append("vertical-align: sub; font-size: smaller;")
    
    # Skill Magnitude
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append(f"color: {colors[smag]};")
    
    return f"<span style='{' '.join(style)}'>{letter}</span>"

# --- State Management ---
if 'vals' not in st.session_state:
    st.session_state.vals = {'dof': 2, 'data': [[0,0,0,0,0] for _ in range(4)]}

# --- UI Setup ---
dof_idx = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], index=st.session_state.vals['dof'])
st.session_state.vals['dof'] = int(dof_idx)

cols = st.columns(4)
labels = ["PL = Practicality", "PN = Protocol", "PS = Principal", "PR = Purpose"]
inputs = {}

for i, col in enumerate(cols):
    with col:
        st.subheader(labels[i])
        inputs[f"lp{i}"] = st.selectbox(f"{labels[i][:2]} L-Pol", ["+", "-"], index=st.session_state.vals['data'][i][0])
        inputs[f"mp{i}"] = st.selectbox(f"{labels[i][:2]} M-Pol", [" ", "+", "-"], index=st.session_state.vals['data'][i][1])
        inputs[f"mm{i}"] = st.selectbox(f"{labels[i][:2]} M-Mag", ["1", "2", "3"], index=st.session_state.vals['data'][i][2])
        inputs[f"sp{i}"] = st.selectbox(f"{labels[i][:2]} S-Pol", [" ", "+", "-"], index=st.session_state.vals['data'][i][3])
        inputs[f"sm{i}"] = st.selectbox(f"{labels[i][:2]} S-Mag", ["1", "2", "3", "4", "5", "6"], index=st.session_state.vals['data'][i][4])

# --- Randomization ---
if st.button("Randomize All"):
    st.session_state.vals['dof'] = random.randint(0, 4)
    # Fixed range to 4 to match UI columns
    st.session_state.vals['data'] = [
        [random.randint(0,1), random.randint(0,2), random.randint(0,2), random.randint(0,2), random.randint(0,5)] 
        for _ in range(4)
    ]
    st.rerun()

# --- Execution ---
if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, 
               "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    
    html_output = ""
    for i, label in enumerate(labels):
        key = label[:2] # Extracts "PL", "PN", etc from "PL = Practicality"
        letter = mapping[key][inputs[f"lp{i}"]]
        html_output += apply_styles(letter, inputs[f"lp{i}"], inputs[f"mp{i}"], inputs[f"mm{i}"], inputs[f"sp{i}"], inputs[f"sm{i}"], str(st.session_state.vals['dof']))
    
    st.markdown(f"<div style='font-size: 80px; text-align: center;'>{html_output}</div>", unsafe_allow_html=True)