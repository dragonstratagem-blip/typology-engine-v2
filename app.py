import streamlit as st
import random

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
    st.header("Input Controls")
    dof_val = st.selectbox("Degree of Freedom (0-4)", ["0", "1", "2", "3", "4"], key='dof')
    
    labels = ["PL = Practicality", "PN = Protocol", "PS = Principal", "PR = Purpose"]
    inputs = {}
    
    for i in range(4):
        st.subheader(labels[i])
        inputs[f"lp{i}"] = st.selectbox(f"{labels[i][:2]} Letter-Polarity (+ or -)", ["+", "-"], key=f"lp{i}")
        inputs[f"mp{i}"] = st.selectbox(f"{labels[i][:2]} Influence-Polarity (+ or- or nul)", [" ", "+", "-"], key=f"mp{i}")
        inputs[f"mm{i}"] = st.selectbox(f"{labels[i][:2]} Influence-Magnitude (1-3)", ["1", "2", "3"], key=f"mm{i}")
        inputs[f"sp{i}"] = st.selectbox(f"{labels[i][:2]} Capacity-Polarity (+ or- or nul)", [" ", "+", "-"], key=f"sp{i}")
        inputs[f"sm{i}"] = st.selectbox(f"{labels[i][:2]} Capacity-Magnitude (1-6)", ["1", "2", "3", "4", "5", "6"], key=f"sm{i}")

# --- index calculation ---
current_index = calculate_index(inputs, int(dof_val))

# --- main page execution ---
st.write(f"### {current_index:,} of 55,099,802,880 combinations")
st.title("Typology Primer Codification Engine")

# use the on_click parameter to trigger the callback
st.button("Randomize All", on_click=randomize_data)

if st.button("Generate"):
    mapping = {"PL": {"+":"E", "-":"I"}, "PN": {"+":"S", "-":"N"}, "PS": {"+":"T", "-":"F"}, "PR": {"+":"J", "-":"P"}}
    html_output = ""
    for i, label in enumerate(labels):
        key = label[:2]
        letter = mapping[key][inputs[f"lp{i}"]]
        html_output += apply_styles(letter, inputs[f"lp{i}"], inputs[f"mp{i}"], inputs[f"mm{i}"], inputs[f"sp{i}"], inputs[f"sm{i}"], dof_val)
    st.markdown(f"<div style='font-size: clamp(50px, 15vw, 300px); text-align: center; line-height: 1.2;'>{html_output}</div>", unsafe_allow_html=True)
    
    # --- glossary section ---
    st.markdown("---")
    st.markdown("### Glossary of Typology Primers")
    st.markdown("""
    * **PL (Practicality)**: Merriam-Webster's Dictionary definition 1: and (Practical) definition 1 a: the quality or state of being of relating to, or manifested in practice or action : not theoretical or ideal.
        * **+PL = (E)**: Extraversion: The use of practicality in decision making.
        * **-PL = (I)**: Introversion: the lack of practicality and decision making.
    * **PN (Protocol)**: Merriam-Webster's Dictionary definition 1 a: a system of rules that explain the correct conduct and procedures to be followed in formal situations.
        * **+PN = (S)**: Sensing: The use of protocol in decision making.
        * **-PN = (N)**: Intuition: the lack of protocol in decision making.
    * **PS (Principal)**: Merriam-Webster's Dictionary definition 1 a: a comprehensive and fundamental law, doctrine, or assumption.
        * **+PS = (T)**: Thinking: The use of principles in decision making.
        * **-PS = (F)**: Feeling: the lack of principles in decision making.
    * **PR (Purpose)**: Merriam-Webster's Dictionary definition 1 c: the aim or goal of a person.
        * **+PR = (J)**: Judging: the use of purpose and decision making.
        * **-PR = (P)**: Perceiving: The lack of purpose in decision making.
        
    ### Additional Definitions
    * **Letter-Polarity**: Is either + or - before the letter code for the primer of the personality Trait Duality. The letters of the Myers-Briggs personality types, such as E, I, S, N, T, F, J, and P, are determined by the polarity applied to 1 of 4 primer codes.
    * **Influence-Polarity**: Is either +, -, or null, placed before the Influence-Magnitude number, where influence is the effect the primer has on the person's personality. The visual representation is an underline for plus (+), a strikethrough for minus (-), and plain text for null.
    * **Influence-Magnitude**: Is a range of 1 to 3 indicating how much the primer influences the person's personality. The visual representation is italic for an influence of 1, standard text for an influence of 2, and bold for an influence of 3.
    * **Capacity-Polarity**: Is either +, -, or null before the Capacity-Magnitude number, where capacity is the effect that the person's personality has on the primer. The visual representation is superscript for plus (+), subscript for minus (-), and standard alignment for null.
    * **Capacity-Magnitude**: Is a range of 1 to 6 indicating how much the person's personality affects the primer. The visual representation is red text for a capacity of 1, orange text for 2, yellow text for 3, green text for 4, blue text for 5, and purple text for 6.
    """)