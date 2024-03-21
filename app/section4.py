import rai_guide as rai_guide
import pipeline as pipeline
import helper

def section4(st):
    st.subheader("Fairness Considerations")

    st.write("For the following Fairness Goal, \n1) Select the relevant stakeholder(s) (e.g., system user, person impacted by the system); \n2) Consider potential AI related harms and consequences that may arise from the system; and \n3) Describe your ideas for mitigations.")

    st.write("#### Goal F2: Allocation of resources and opportunities")

    st.write(f"_This Goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare. Consider: {rai_guide.f2_guide}_")

    st.markdown("_When considering this fairness goal, think about different demographic group of stakeholders and consider marginalized groups._", help="**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.\n\n**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")

    all_stakeholders = helper.get_stakeholders(st)

    st.session_state['f2_selected_stakeholders'] = st.multiselect(
        'Which stakeholders will be affected?',
        all_stakeholders,
        st.session_state.get('f2_selected_stakeholders', [])
    )

    st.write("For each identified stakeholder, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.")
    st.session_state[f'goal_f2_2'] =  st.text_area("Describe any potential harms ", value=st.session_state.get(f"goal_f2_2", ""))

    st.write("After identifying potential harms, propose practical strategies to mitigate these issues. Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness. List the actions you might take to mitigate the potential harms and fairness issues you have identified.")
    st.markdown("Examples of mitigation strategies for 'Allocation of resources and opportunities' realted harms include evaluating the data sets and the system then modifying the system to minimize differences in the allocation of resources and opportunities between identified demographic groups.", help="For example, a hiring system that scans resumes and recommends candidates for hiring trained on historical data tends to be biased toward male candidates. The system can be evaluated and modified to reduce unfair allocation of opportunities.")
    st.session_state[f'goal_f2_3'] =  st.text_area("Describe your ideas for mitigations ", value=st.session_state.get(f"goal_f2_3", ""))

    