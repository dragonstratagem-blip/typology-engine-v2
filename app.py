import streamlit as st
import random

# --- custom css injection ---
st.markdown("""
<style>
[data-testid="stSidebar"] label p,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] h3 {
    font-size: 200% !important;
    font-weight: bold !important;
    color: #FFEF00 !important;
}
</style>
""", unsafe_allow_html=True)

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
        st.session_state[f"mm{i}"] = random