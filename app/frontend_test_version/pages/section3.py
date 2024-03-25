import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu

st.subheader("Fairness Considerations")

st.write("For the following Fairness Goal, \n1) Select the relevant stakeholder(s) (e.g., system user, person impacted by the system); \n2) Consider potential AI related harms and consequences that may arise from the system; and \n3) Describe your ideas for mitigations.")

st.write("#### Goal F1: Quality of service")

st.write(f"_This Goal applies to AI systems when system users or people impacted by the system with different demographic characteristics might experience differences in quality of service that can be remedied by building the system differently. Consider: {rai_guide.f1_guide}_")

st.markdown("_When considering this fairness goal, think about different demographic group of stakeholders and consider marginalized groups._", help="**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.\n\n**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")

all_stakeholders = helper.get_stakeholders(st)

# Start generating F3 scenarios as soon as stakeholders are filled & user moves on the section 3
f3_enum = helper.Task.F3.value
sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"
if all_stakeholders != [] and f'{f3_enum}_task_status' not in st.session_state:
    helper.send_req(st, sys_info, f3_enum, all_stakeholders)
    print("sending request for f3")

st.markdown(f"For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]), consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.")
st.session_state[f'goal_f1_2'] =  st.text_area("Describe any potential harms ", value=st.session_state.get(f"goal_f1_2", ""))

st.write("After identifying potential harms, propose practical strategies to mitigate these issues. Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness. List the actions you might take to mitigate the potential harms and fairness issues you have identified.")
st.markdown("Examples of mitigation strategies for 'Quality of Service' realted harms include evaluating the data sets and the system, then modifying the system to improve system performance for affected demographic groups while minimizing performance differences between identified demographic groups.", help="For example, people who speak language varieties that are underrepresented in the training data may experience worse quality of service for a voice transcription system. The system can be evaluated and modified to improve quality of service for these demographic groups.")
st.session_state[f'goal_f1_3'] =  st.text_area("Describe your ideas for mitigations ", value=st.session_state.get(f"goal_f1_3", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        st.switch_page("pages/section4.py")

menu(st)
