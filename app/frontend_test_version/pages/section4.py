import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu


st.subheader("Fairness Considerations - Allocation of resources and opportunities")

st.write("In this section, consider potential AI related harms and consequences that may arise from the system and describe your ideas for mitigations")

st.markdown(":closed_book: **Definition:** The <ins>Allocation of resources and opportunities</ins> fairness goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare.", unsafe_allow_html=True)

st.write("#### Potential Harms")

st.markdown(f":grey_question: **Hint:** {rai_guide.f2_guide} Consider marginalized groups and think about different demographic group of stakeholders.", help="**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.\n\n**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")

all_stakeholders = helper.get_stakeholders(st)

# Start generating F3 scenarios as soon as stakeholders are filled & user moves on the section 3
f3_enum = helper.Task.F3.value
sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"
if all_stakeholders != [] and f'{f3_enum}_task_status' not in st.session_state:
    helper.send_req(st, sys_info, f3_enum, all_stakeholders)
    print("sending request for f3")

st.session_state[f'goal_f2_2'] =  st.text_area(f":lower_left_ballpoint_pen: **Instruction:** :blue[Describe any potential harms]. For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]) that are relevant, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.", value=st.session_state.get(f"goal_f2_2", ""))

st.write("#### Mitigations")

st.write("After identifying potential harms, propose practical strategies to mitigate these issues.")

st.markdown(":grey_question: **Hint:** Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness.", help="Examples of mitigation strategies for 'Allocation of resources and opportunities' realted harms include evaluating the data sets and the system then modifying the system to minimize differences in the allocation of resources and opportunities between identified demographic groups.\n\n e.g. A hiring system that scans resumes and recommends candidates for hiring trained on historical data tends to be biased toward male candidates. The system can be evaluated and modified to reduce unfair allocation of opportunities.")

st.session_state[f'goal_f2_3'] =  st.text_area(":lower_left_ballpoint_pen: **Instruction:** :blue[Describe your ideas for mitigations]. List the actions you might take to mitigate the potential harms and fairness issues you have identified.", value=st.session_state.get(f"goal_f2_3", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        st.switch_page("pages/section5.py")

menu(st)
