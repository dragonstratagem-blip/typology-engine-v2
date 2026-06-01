import streamlit as st
import random

# --- page configuration ---
st.set_page_config(layout="wide")

# --- calculation logic ---
def calculate_index(inputs, dof_val):
    col_totals = []
    for i in range(4):
        lp = ["+", "-"].index(inputs[f"lp{i}"])
        mp = [" ", "+", "-"].index(inputs[f"mp{i}"])
        mm = ["1", "2", "3"].index(inputs[f"mm{i}"])
        sp = [" ", "+", "-"].index(inputs[f"sp{i}"])
        sm = ["1", "2", "3", "4", "5", "6"].index(inputs[f"sm{i}"])
        
        val = sm + (6 * (sp + (3 * (mm + (3 * (mp + (3 * lp)))))))
        col_totals.append(val)
    
    total = col_totals[0] + (324 * col_totals[1]) + (324**2 * col_totals[2]) + (324**3 * col_totals[3])
    
    return (total * 5) + dof_val

# --- styling logic ---
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

# --- callback function for randomization ---
def randomize_data():
    st.session_state.dof = str(random.randint(0, 4))
    for i in range(4):
        st.session_state[f"lp{i}"] = random.choice(["+", "-"])
        st.session_state[f"mp{i}"] = random.choice([" ", "+", "-"])
        st.session_state[f"mm{i}"] = random.choice(["1", "2", "3"])
        st.session_state[f"sp{i}"] = random.choice([" ", "+", "-"])
        st.session_state[f"sm{i}"] = random.choice(["1", "2", "3", "4", "5", "6"])

# --- state management ---
if 'initialized' not in st.session_state:
    st.session_state.dof = "2"
    for i in range(4):
        st.session_state[f"lp{i}"] = "+"
        st.session_state[f"mp{i}"] = " "
        st.session_state[f"mm{i}"] = "1"
        st.session_state[f"sp{i}"] = " "
        st.session_state[f"sm{i}"] = "1"
    st.session_state.initialized = True

# --- sidebar inputs ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>Input Controls</h2>", unsafe_allow_html=True)
    dof_val = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], key='dof')
    
    labels = ["PL = Practicality", "PN = Protocol", "PS = Principal", "PR = Purpose"]
    inputs = {}
    
    for i in range(4):
        st.markdown(f"<h3 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>{labels[i]}</h3>", unsafe_allow_html=True)
        inputs[f"lp{i}"] = st.selectbox(f"{labels[i][:2]} Letter-Polarity (+ or -)", ["+", "-"], key=f"lp{i}")
        inputs[f"mp{i}"] = st.selectbox(f"{labels[i][:2]} Influence-Polarity (+ or- or nul)", [" ", "+", "-"], key=f"mp{i}")
        inputs[f"mm{i}"] = st.selectbox(f"{labels[i][:2]} Influence-Magnitude (1-3)", ["1", "2", "3"], key=f"mm{i}")
        inputs[f"sp{i}"] = st.selectbox(f"{labels[i][:2]} Capacity-Polarity (+ or- or nul)", [" ", "+", "-"], key=f"sp{i}")
        inputs[f"sm{i}"] = st.selectbox(f"{labels[i][:2]} Capacity-Magnitude (1-6)", ["1", "2", "3", "4", "5", "6"], key=f"sm{i}")

# --- index calculation ---
current_index = calculate_index(inputs, int(dof_val))

# --- main page execution ---
st.markdown(f"""
<h3 style='font-size: 200%; margin-bottom: 0px;'>
    <span style='color: #FF1493;'>{current_index:,}</span> 
    <span style='color: white;'>OF</span> 
    <span style='color: #8A2BE2;'>55,099,80