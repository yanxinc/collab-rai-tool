import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu

st.subheader("Fairness Considerations - Minimization of stereotyping, demeaning, and erasing outputs")

st.write("In this section, consider potential AI related harms and consequences that may arise from the system and describe your ideas for mitigations")

st.markdown(":closed_book: **Definition:** The <ins>Minimization of stereotyping, demeaning, and erasing outputs</ins> fairness goal applies to AI systems when system outputs include descriptions, depictions, or other representations of people, cultures, or society.", unsafe_allow_html=True)

st.write("#### Potential Harms")

helper.potential_harms_hint(st, rai_guide.f3_guide)

all_stakeholders = helper.get_stakeholders(st)

# Start generating F2 scenarios as soon as stakeholders are filled & user moves on the section 3
f_enum = helper.Task.F2.value
if 'all_system_info' in st.session_state and st.session_state['all_system_info'] != "":
    sys_info = st.session_state['all_system_info']
else:
    sys_info = f"I am building the following AI application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"

if all_stakeholders != [] and f'{f_enum}_task_status' not in st.session_state:
    helper.send_req(st, sys_info, f_enum, all_stakeholders)
    print("sending request for f2")

st.session_state[f'goal_f3_2'] =  st.text_area(f":lower_left_ballpoint_pen: **Instruction: Describe any potential harms**. For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]) that are relevant, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.  ", value=st.session_state.get(f"goal_f3_2", ""))

st.write("#### Mitigations")

st.write("After identifying potential harms, propose practical strategies to mitigate these issues.")

st.markdown(":grey_question: **Hint:** Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness.", help="Examples of mitigation strategies for 'Minimization of stereotyping, demeaning, and erasing outputs' realted harms include developing a rigorous understanding of how different demographic groups are represented within the AI system and modifying the system to minimize harmful outputs.\n\n e.g. An image search system that predominantly returns images of men in response to the query “chief executive officer” may underrepresent non-male chief executive officers. To mitigate this, the system can be modified to provide more representative outputs.")

st.session_state[f'goal_f3_3'] =  st.text_area(":lower_left_ballpoint_pen: **Instruction: Describe your ideas for mitigations**. List the actions you might take to mitigate the potential harms and fairness issues you have identified.  ", value=st.session_state.get(f"goal_f3_3", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        st.switch_page("pages/section4.py")

menu(st)
