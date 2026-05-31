import streamlit as st
import random

# --- Calculation Logic ---
def calculate_index(inputs):
    # Mapping dropdown options to 0-based indices
    # lp: 2, mp: 3, mm: 3, sp: 3, sm: 6
    # Base 324 per column
    col_totals = []
    for i in range(4):
        lp = ["+", "-"].index(inputs[f"lp{i}"])
        mp = [" ", "+", "-"].index(inputs[f"mp{i}"])
        mm = ["1", "2", "3"].index(inputs[f"mm{i}"])
        sp = [" ", "+", "-"].index(inputs[f"sp{i}"])
        sm = ["1", "2", "3", "4", "5", "6"].index(inputs[f"sm{i}"])
        
        # Flatten column into a single integer 0-323
        val = sm + (6 * (sp + (3 * (mm + (3 * (mp + (3 * lp)))))))
        col_totals.append(val)
    
    # Calculate total index in base-324
    total = col_totals[0] + (324 * col_totals[1]) + (324**2 * col_totals[2]) + (324**3 * col_totals[3])
    return total

# --- Styling Logic ---
def apply_styles(letter, pol, mag_pol, mag_val, spol, smag, dof_val):
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = [f"font-family: {fonts[dof_val]};"]
    if pol == "+": style.append("text-decoration: underline;")
    elif pol == "-": style.append("text-decoration: line-through;")
    if mag_pol == "+": style.append("font-weight: bold;")
    elif mag_pol == "-": style.append("font-style: italic;")
    if spol == "+": style.append("vertical-align: super; font-size: smaller;")
    elif spol == "-": style.append("vertical-align: sub; font-size: smaller;")
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append(f"color: {colors[smag]};")
    return f"<span style='{' '.join(style)}'>{letter}</span>"

# --- State Management ---
if 'vals' not in st.session_state:
    st.session_state.vals = {'dof': 2, 'data': [[0,0,0,0,0] for _ in range(4)]}

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("Input Controls")
    dof_idx = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], index=st.session_state.vals['dof'])
    st.session_state.vals['dof'] = int(dof_idx)
    labels = ["PL = Practicality", "PN = Protocol", "PS = Principal", "PR = Purpose"]
    inputs = {}
    for i in range(4):
        st.subheader(labels[i])
        inputs[f"lp{i}"] = st.selectbox(f"{labels[i][:2]} L-Pol", ["+", "-"], index=st.session_state.vals['data'][i][0])
        inputs[f"mp{i}"] = st.selectbox(f"{labels[i][:2]} M-Pol", [" ", "+", "-"], index=st.session_state.vals['data'][i][1])
        inputs[f"mm{i}"] = st.selectbox(f"{labels[i][:2]} M-Mag", ["1", "2", "3"], index=st.session_state.vals['data'][i][2])
        inputs[f"sp{i}"] = st.selectbox(f"{labels[i][:2]} S-Pol", [" ", "+", "-"], index=st.session_state.vals['data'][i][3])
        inputs[f"sm{i}"] = st.selectbox(f"{labels[i][:2]} S-Mag", ["1", "2", "3", "4", "5", "6"], index=st.session_state.vals['data'][i][4])

# --- Index Calculation ---
current_index = calculate_index(inputs)

# --- Main Page Execution ---
st.write(f"### {current_index:,} of 55,000,000,000 combinations")
st.title("Typology Codification Engine")

if st.button("Randomize All"):
    st.session_state.vals['dof'] = random.randint(0, 4)
    st.session_state.vals['data'] = [[random.randint(0,1), random.randint(0,2), random.randint(0,2), random.randint(0,2), random.randint(0,5)] for _ in range(4)]
    st.rerun()

if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    html_output = ""
    for i, label in enumerate(labels):
        key = label[:2]
        letter = mapping[key][inputs[f"lp{i}"]]
        html_output += apply_styles(letter, inputs[f"lp{i}"], inputs[f"mp{i}"], inputs[f"mm{i}"], inputs[f"sp{i}"], inputs[f"sm{i}"], str(st.session_state.vals['dof']))
    st.markdown(f"<div style='font-size: clamp(50px, 15vw, 300px); text-align: center; line-height: 1.2;'>{html_output}</div>", unsafe_allow_html=True)