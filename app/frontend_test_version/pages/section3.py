import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu

st.subheader("Fairness Considerations - Quality of service")

st.write("In this section, consider potential AI related harms and consequences that may arise from the system and describe your ideas for mitigations")

st.markdown(":closed_book: **Definition:** The <ins>Quality of Service</ins> fairness goal applies to AI systems when system users or people impacted by the system with different demographic characteristics might experience differences in quality of service that can be remedied by building the system differently.", unsafe_allow_html=True)

st.write("#### Potential Harms")

st.markdown(f":grey_question: **Hint:** {rai_guide.f1_guide} Consider marginalized groups and think about different demographic group of stakeholders.", help="**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.\n\n**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")

all_stakeholders = helper.get_stakeholders(st)

st.session_state[f'goal_f1_2'] =  st.text_area(f":lower_left_ballpoint_pen: **Instruction:** :blue[Describe any potential harms]. For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]) that are relevant, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use. ", value=st.session_state.get(f"goal_f1_2", ""))

st.write("#### Mitigations")

st.write("After identifying potential harms, propose practical strategies to mitigate these issues.")

st.markdown(":grey_question: **Hint:** Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness.", help="Examples of mitigation strategies for 'Quality of Service' realted harms include evaluating the data sets and the system, then modifying the system to improve system performance for affected demographic groups while minimizing performance differences between identified demographic groups.\n\n e.g. People who speak language varieties that are underrepresented in the training data may experience worse quality of service for a voice transcription system. The system can be evaluated and modified to improve quality of service for these demographic groups.")

st.session_state[f'goal_f1_3'] =  st.text_area(":lower_left_ballpoint_pen: **Instruction:** :blue[Describe your ideas for mitigations]. List the actions you might take to mitigate the potential harms and fairness issues you have identified. ", value=st.session_state.get(f"goal_f1_3", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        st.switch_page("pages/section4.py")

menu(st)
