import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu
from streamlit_feedback import streamlit_feedback

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

st.subheader("Fairness Considerations - Allocation of resources and opportunities")

st.write("In this section, consider potential AI related harms and consequences that may arise from the system and describe your ideas for mitigations")

st.markdown(":closed_book: **Definition:** The <ins>Allocation of resources and opportunities</ins> fairness goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare.", unsafe_allow_html=True)

st.write("#### Potential Harms")

helper.potential_harms_hint(st, rai_guide.f2_guide)

all_stakeholders = helper.get_stakeholders(st)

f_enum = helper.Task.F2.value

if 'all_system_info' in st.session_state and st.session_state['all_system_info'] != "":
    sys_info = st.session_state['all_system_info']
else:
    sys_info = f"I am building the following AI application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"

if all_stakeholders != [] and f'{f_enum}_task_status' not in st.session_state:
    helper.send_req(st, sys_info, f_enum, all_stakeholders)
    print("sending request for f2")

f2_brainstorm = st.button("Help me brainstorm scenarios concerning Allocation of resources and opportunities", use_container_width=True, type='primary')

if f'f2_clicked' in st.session_state and f'{f_enum}_result' in st.session_state:
    with st.container(border=True):
        helper.write_scenarios(st, f_enum, streamlit_feedback)
        helper.display_buttons(st, f_enum, sys_info, all_stakeholders)

if f2_brainstorm:
    if all_stakeholders != []:
        st.session_state[f'f2_clicked'] = True
        helper.wait_response(st, f_enum)
    else:
        st.write("Please fill in stakeholders first")


st.session_state[f'goal_f2_2'] =  st.text_area(f":lower_left_ballpoint_pen: **Instruction: Describe any potential harms**. For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]) that are relevant, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.", value=st.session_state.get(f"goal_f2_2", ""))

st.write("#### Mitigations")

st.write("After identifying potential harms, propose practical strategies to mitigate these issues.")

st.markdown(":grey_question: **Hint:** Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness.", help="Examples of mitigation strategies for 'Allocation of resources and opportunities' realted harms include evaluating the data sets and the system then modifying the system to minimize differences in the allocation of resources and opportunities between identified demographic groups.\n\n e.g. A hiring system that scans resumes and recommends candidates for hiring trained on historical data tends to be biased toward male candidates. The system can be evaluated and modified to reduce unfair allocation of opportunities.")

st.session_state[f'goal_f2_3'] =  st.text_area(":lower_left_ballpoint_pen: **Instruction: Describe your ideas for mitigations**. List the actions you might take to mitigate the potential harms and fairness issues you have identified.", value=st.session_state.get(f"goal_f2_3", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        st.switch_page("pages/section5.py")

menu(st)