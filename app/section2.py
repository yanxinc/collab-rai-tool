import pandas as pd
import rai_guide as rai_guide
import pipeline as pipeline

def section2(st, i):
    st.header(f"Section 2.{i}: Intended Uses")

    intended_use = st.session_state.get(f'iu{i}', "").strip()
    intended_use_description = st.session_state.get(f'iu{i}_des', "").strip()
    sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An intended use is {intended_use}. The description of this indented use is {intended_use_description}"

    st.write(f"Intended use #1 : **{intended_use if intended_use != '' else '[Name of intended use]'}**")

    st.subheader("Stakeholders, potential benefits, and potential harms")
    st.write("**2.2** _Identify the system's stakeholders for this intended use. Then, for each stakeholder, document the potential benefits and potential harms. For more information, including prompts, see the Impact Assessment Guide._")
    stakeholder_df = st.data_editor(
        pd.DataFrame(
            [
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
                {"Stakeholders": "", "Potential system benefits": "", "Potential system harms":""},
            ]
        ),  num_rows="dynamic", hide_index=False)
    
    st.session_state[f'stakeholders_{i}'] = stakeholder_df


    with st.expander("Stakeholders Identification Guide"):
        st.write(rai_guide.stakeholder_def)

        if f"stakeholders_result_{i}" in st.session_state and st.session_state[f"stakeholders_result_{i}"]:
            st.write(st.session_state[f"stakeholders_result_{i}"])

        stakeholder_button = st.button("Brainstorm stakeholders")

        if stakeholder_button:
            if intended_use != '':
                st.session_state[f"stakeholders_result_{i}"] = pipeline.stakeholders(sys_info)
                st.write(st.session_state[f"stakeholders_result_{i}"])
            else:               
                st.write("Please fill in an inteded use first")

    st.subheader("Fairness considerations")
    st.write("**2.4** _For each Fairness Goal that applies to the system, 1) identify the relevant stakeholder(s) (e.g., system user, person impacted by the system); 2) identify any demographic groups, including marginalized groups, that may require fairness considerations; and 3) prioritize these groups for fairness consideration and explain how the fairness consideration applies. If the Fairness Goal does not apply to the system, enter “N/A” in the first column._")

    with st.expander("General Fairness Goals Guide"):
        st.write("**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.")
        st.write("**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")

        st.write(rai_guide.f_2)

    st.write("#### Goal F1: Quality of service")
    st.write("_This Goal applies to AI systems when system users or people impacted by the system with different demographic characteristics might experience differences in quality of service that can be remedied by building the system differently. If this Goal applies to the system, complete the table below describing the appropriate stakeholders for this intended use._")
    st.session_state[f'goal_f1_1_{i}'] =  st.text_input("Which stakeholder(s) will be affected?", value=st.session_state.get(f"goal_f1_1_{i}", ""))
    st.session_state[f'goal_f1_2_{i}'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal?", value=st.session_state.get(f"goal_f1_2_{i}", ""))
    st.session_state[f'goal_f1_3_{i}'] =  st.text_area("Explain how each demographic group might be affected.", value=st.session_state.get(f"goal_f1_3_{i}", ""))

    with st.expander("Goal F1 Guide"):
        with st.form("f1_guide"):
            st.write(rai_guide.f1_guide)
        
            f1_stakeholders_on = st.toggle('Generate stakeholder for me')
            f1_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning Quality of Service")

            if f"f1_scenarios_{i}" in st.session_state:
                st.write(st.session_state[f"f1_scenarios_{i}"])

            if f1_brainstorm:
                if f1_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f1')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f1', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state[f"f1_scenarios_{i}"] = res

    st.write("#### Goal F2: Allocation of resources and opportunities")
    st.write("_This Goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare. If this Goal applies to the system, complete the table below describing the appropriate stakeholders for this intended use._")
    st.session_state[f'goal_f2_1_{i}'] =  st.text_input("Which stakeholder(s) will be affected? ", value=st.session_state.get(f"goal_f2_1_{i}", ""))
    st.session_state[f'goal_f2_2_{i}'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal? ", value=st.session_state.get(f"goal_f2_2_{i}", ""))
    st.session_state[f'goal_f2_3_{i}'] =  st.text_area("Explain how each demographic group might be affected. ", value=st.session_state.get(f"goal_f2_3_{i}", ""))
    
    with st.expander("Goal F2 Guide"):
        with st.form("f2_guide"):
            st.write(rai_guide.f2_guide)
        
            f2_stakeholders_on = st.toggle('Generate stakeholder for me')
            f2_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning Allocation of resources and opportunities Considerations")

            if f"f2_scenarios_{i}" in st.session_state:
                st.write(st.session_state[f"f2_scenarios_{i}"])

            if f2_brainstorm:
                if f2_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f2')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f2', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state[f"f2_scenarios_{i}"] = res
                print("f2_scenarios updated")

    st.write("#### Goal F3: Minimization of stereotyping, demeaning, and erasing outputs")
    st.write("_This Goal applies to AI systems when system outputs include descriptions, depictions, or other representations of people, cultures, or society. If this Goal applies to the system, complete the table below describing the appropriate stakeholders for this intended use._")
    st.session_state[f'goal_f3_1_{i}'] =  st.text_input("Which stakeholder(s) will be affected?  ", value=st.session_state.get(f"goal_f3_1_{i}", ""))
    st.session_state[f'goal_f3_2_{i}'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal?  ", value=st.session_state.get(f"goal_f3_2_{i}", ""))
    st.session_state[f'goal_f3_3_{i}'] =  st.text_area("Explain how each demographic group might be affected.  ", value=st.session_state.get(f"goal_f3_3_{i}", ""))

    with st.expander("Goal F3 Guide"):
        with st.form("f3_guide"):
            st.write(rai_guide.f3_guide)
        
            f3_stakeholders_on = st.toggle('Generate stakeholder for me')
            f3_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning stereotyping, demeaning, and erasing outputs")

            if f"f3_scenarios_{i}" in st.session_state:
                st.write(st.session_state[f"f3_scenarios_{i}"])

            if f3_brainstorm:
                if f3_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f3')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f3', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state[f"f3_scenarios_{i}"] = res

