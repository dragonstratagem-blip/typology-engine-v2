import streamlit as st
import random

# --- Page Config ---
st.set_page_config(layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
div.stButton > button {
    font-size: 20px !important;
    padding: 15px 30px !important;
    width: 100%;
}
div.stButton:nth-of-type(1) > button {
    background-color: #FFD700 !important;
    color: #8B4513 !important;
}
div.stButton:nth-of-type(2) > button {
    background-color: #C0C0C0 !important;
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)

# --- Logic ---
def calculate_index(inputs, dof_val):
    col_totals = []
    for i in range(4):
        lp = ["+", "-"].index(inputs["lp" + str(i)])
        mp = [" ", "+", "-"].index(inputs["mp" + str(i)])
        mm = ["1", "2", "3"].index(inputs["mm" + str(i)])
        sp = [" ", "+", "-"].index(inputs["sp" + str(i)])
        sm = ["1", "2", "3", "4", "5", "6"].index(inputs["sm" + str(i)])
        val = sm + (6 * (sp + (3 * (mm + (3 * (mp + (3 * lp)))))))
        col_totals.append(val)
    total = col_totals[0] + (324 * col_totals[1]) + (324**2 * col_totals[2]) + (324**3 * col_totals[3])
    return (total * 5) + dof_val

def apply_styles(letter, pol, mag_pol, spol, smag, dof_val):
    fonts = {"4":"serif", "3":"sans-serif", "2":"fantasy", "1":"cursive", "0":"monospace"}
    style = ["font-family: " + fonts[dof_val] + ";"]
    if pol == "+": style.append("text-decoration: underline;")
    elif pol == "-": style.append("text-decoration: line-through;")
    if mag_pol == "+": style.append("font-weight: bold;")
    elif mag_pol == "-": style.append("font-style: italic;")
    if spol == "+": style.append("vertical-align: super; font-size: smaller;")
    elif spol == "-": style.append("vertical-align: sub; font-size: smaller;")
    colors = {"6":"purple", "5":"blue", "4":"green", "3":"yellow", "2":"orange", "1":"red"}
    style.append("color: " + colors[smag] + ";")
    return "<span style='" + " ".join(style) + "'>" + letter + "</span>"

def randomize_data():
    st.session_state.dof = str(random.randint(0, 4))
    for i in range(4):
        st.session_state["lp" + str(i)] = random.choice(["+", "-"])
        st.session_state["mp" + str(i)] = random.choice([" ", "+", "-"])
        st.session_state["mm" + str(i)] = random.choice(["1", "2", "3"])
        st.session_state["sp" + str(i)] = random.choice([" ", "+", "-"])
        st.session_state["sm" + str(i)] = random.choice(["1", "2", "3", "4", "5", "6"])

if 'initialized' not in st.session_state:
    st.session_state.dof = "2"
    for i in range(4):
        st.session_state["lp" + str(i)] = "+"
        st.session_state["mp" + str(i)] = " "
        st.session_state["mm" + str(i)] = "1"
        st.session_state["sp" + str(i)] = " "
        st.session_state["sm" + str(i)] = "1"
    st.session_state.initialized = True

# --- UI ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>Input Controls</h2>", unsafe_allow_html=True)
    dof_val = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], key='dof')
    labels = ["PL", "PN", "PS", "PR"]
    inputs = {}
    for i in range(4):
        st.markdown("<h3 style='font-size: 150%; font-weight: bold; color: #FFEF00;'>" + labels[i] + "</h3>", unsafe_allow_html=True)
        inputs["lp" + str(i)] = st.selectbox("Letter-Polarity", ["+", "-"], key="lp" + str(i))
        inputs["mp" + str(i)] = st.selectbox("Influence-Polarity", [" ", "+", "-"], key="mp" + str(i))
        inputs["mm" + str(i)] = st.selectbox("Influence-Magnitude", ["1", "2", "3"], key="mm" + str(i))
        inputs["sp" + str(i)] = st.selectbox("Capacity-Polarity", [" ", "+", "-"], key="sp" + str(i))
        inputs["sm" + str(i)] = st.selectbox("Capacity-Magnitude", ["1", "2", "3", "4", "5", "6"], key="sm" + str(i))

current_index = calculate_index(inputs, int(dof_val))
st.markdown("<h3 style='font-size: 200%; margin-bottom: 0px;'><span style='color: #FF1493;'>" + str(current_index) + "</span> <span style='color: white;'>OF</span> <span style='color: #8A2BE2;'>55,099,802,880</span> <span style='color: white;'>COMBINATIONS</span></h3>", unsafe_allow_html=True)
st.markdown("<h1 style='color: lightblue; font-size: 300%; margin-top: 10px;'>TYPOLOGY PRIMER CODIFICATION ENGINE</h1>", unsafe_allow_html=True)

c1, c2 = st.columns([1, 4])
if c1.button("Randomize All"): randomize_data(); st.rerun()
if c2.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    html_out = ""
    for i in range(4):
        letter = mapping[labels[i]][inputs["lp" + str(i)]]
        html_out += apply_styles(letter, inputs["lp" + str(i)], inputs["mp" + str(i)], inputs["sp" + str(i)], inputs["sm" + str(i)], dof_val)
    st.markdown("<div style='font-size: clamp(50px, 15vw, 300px); text-align: center;'>" + html_out + "</div>", unsafe_allow_html=True)