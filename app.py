import streamlit as st
import random

# --- page configuration ---
st.set_page_config(layout="wide")

# --- custom button/text styling ---
# Using standard triple quotes to avoid f-string confusion
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

# --- calculation logic ---
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

# --- state management ---
if 'initialized' not in st.session_state:
    st.session_state.dof = "2"
    for i in range(4):
        st.session_state["lp" + str(i)] = "+"
        st.session_state["mp" + str(i)] = " "
        st.session_state["mm" + str(i)] = "1"
        st.session_state["sp" + str(i)] = " "
        st.session_state["sm" + str(i)] = "1"
    st.session_state.initialized = True

# --- sidebar inputs ---
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

# --- main page execution ---
current_index = calculate_index(inputs, int(dof_val))
idx_str = f"{current_index:,}"

# Display serial number and combinations
st.markdown("<h3 style='font-size: 200%; margin-bottom: 0px;'><span style='color: #FF1493;'>" + idx_str + "</span> <span style='color: white;'>OF</span> <span style='color: #8A2BE2;'>55,099,802,880 COMBINATIONS</span></h3>", unsafe_allow_html=True)
st.markdown("<h1 style='color: lightblue; font-size: 300%; margin-top: 10px;'>TYPOLOGY PRIMER CODIFICATION ENGINE</h1>", unsafe_allow_html=True)

# Buttons
col1, col2 = st.columns([1, 4])
if col1.button("Randomize All"): randomize_data(); st.rerun()
generate_btn = col2.button("Generate")

if generate_btn:
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    html_output = ""
    for i in range(4):
        letter = mapping[labels[i]][inputs["lp" + str(i)]]
        html_output += apply_styles(letter, inputs["lp" + str(i)], inputs["mp" + str(i)], inputs["sp" + str(i)], inputs["sm" + str(i)], dof_val)
    st.markdown("<div style='font-size: clamp(50px, 15vw, 300px); text-align: center; line-height: 1.2;'>" + html_output + "</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size: 150%; font-weight: bold; color: #FFEF00;">
    <h3>Glossary of Typology Primers</h3>
    <ul><li><b>PL (Practicality)</b>: The quality or state of being of relating to, or manifested in practice or action : not theoretical or ideal.<ul><li><b>+PL = (E)</b>: Extraversion: The use of practicality in decision making.</li><li><b>-PL = (I)</b>: Introversion: the lack of practicality and decision making.</li></ul></li>
    <li><b>PN (Protocol)</b>: A system of rules that explain the correct conduct and procedures to be followed in formal situations.<ul><li><b>+PN = (S)</b>: Sensing: The use of protocol in decision making.</li><li><b>-PN = (N)</b>: Intuition: the lack of protocol in decision making.</li></ul></li>
    <li><b>PS (Principal)</b>: A comprehensive and fundamental law, doctrine, or assumption.<ul><li><b>+PS = (T)</b>: Thinking: The use of principles in decision making.</li><li><b>-PS = (F)</b>: Feeling: the lack of principles in decision making.</li></ul></li>
    <li><b>PR (Purpose)</b>: The aim or goal of a person.<ul><li><b>+PR = (J)</b>: Judging: the use of purpose and decision making.</li><li><b>-PR = (P)</b>: Perceiving: The lack of purpose in decision making.</li></ul></li></ul>
    <h3>Additional Definitions</h3>
    <ul><li><b>Letter-Polarity</b>: Either + or - before the letter code.</li><li><b>Influence-Polarity</b>: Either +, -, or null; visual representation is underline for +, strikethrough for -, and plain for null.</li><li><b>Influence-Magnitude</b>: 1 to 3 range; visual representation is italic (1), standard (2), and bold (3).</li><li><b>Capacity-Polarity</b>: Either +, -, or null; visual representation is superscript for +, subscript for -, and standard for null.</li><li><b>Capacity-Magnitude</b>: 1 to 6 range; visual representation is red(1), orange(2), yellow(3), green(4), blue(5), purple(6).</li></ul>
    </div>
    """, unsafe_allow_html=True)