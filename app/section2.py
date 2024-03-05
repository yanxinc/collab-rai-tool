import pandas as pd
import rai_guide as rai_guide
import pipeline as pipeline

def section2(st, intended_uses_df):
    st.header("Section 2: Intended Uses")

    intended_use1 = intended_uses_df.iloc[0]["Name of intended use(s)"].strip()
    intended_use1_description = intended_uses_df.iloc[0]["Description of intended use(s)"]
    sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An intended use is {intended_use1}. The description of this indented use is {intended_use1_description}"

    st.write(f"Intended use #1 : **{intended_use1 if intended_use1 != '' else '[Name of intended use]'}**")

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
    
    st.session_state['stakeholders'] = stakeholder_df


    with st.expander("Stakeholders Identification Guide"):
        st.write(rai_guide.stakeholder_def)

        if "stakeholders_result" in st.session_state and st.session_state["stakeholders_result"]:
            st.write(st.session_state["stakeholders_result"])

        stakeholder_button = st.button("Brainstorm stakeholders")

        if stakeholder_button:
            if intended_use1 != '':
                st.session_state["stakeholders_result"] = pipeline.stakeholders(sys_info)
                st.write(st.session_state["stakeholders_result"])
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
    st.session_state['goal_f1_1'] =  st.text_input("Which stakeholder(s) will be affected?", value=st.session_state.get("goal_f1_1", ""))
    st.session_state['goal_f1_2'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal?", value=st.session_state.get("goal_f1_2", ""))
    st.session_state['goal_f1_3'] =  st.text_area("Explain how each demographic group might be affected.", value=st.session_state.get("goal_f1_3", ""))

    with st.expander("Goal F1 Guide"):
        with st.form("f1_guide"):
            st.write(rai_guide.f1_guide)
        
            f1_stakeholders_on = st.toggle('Generate stakeholder for me')
            f1_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning Quality of Service")

            if "f1_scenarios" in st.session_state:
                st.write(st.session_state["f1_scenarios"])

            if f1_brainstorm:
                if f1_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f1')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f1', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state["f1_scenarios"] = res

    st.write("#### Goal F2: Allocation of resources and opportunities")
    st.write("_This Goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare. If this Goal applies to the system, complete the table below describing the appropriate stakeholders for this intended use._")
    st.session_state['goal_f2_1'] =  st.text_input("Which stakeholder(s) will be affected? ", value=st.session_state.get("goal_f2_1", ""))
    st.session_state['goal_f2_2'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal? ", value=st.session_state.get("goal_f2_2", ""))
    st.session_state['goal_f2_3'] =  st.text_area("Explain how each demographic group might be affected. ", value=st.session_state.get("goal_f2_3", ""))
    
    with st.expander("Goal F2 Guide"):
        with st.form("f2_guide"):
            st.write(rai_guide.f2_guide)
        
            f2_stakeholders_on = st.toggle('Generate stakeholder for me')
            f2_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning Allocation of resources and opportunities Considerations")

            if "f2_scenarios" in st.session_state:
                st.write(st.session_state["f2_scenarios"])

            if f2_brainstorm:
                if f2_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f2')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f2', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state["f2_scenarios"] = res
                print("f2_scenarios updated")

    st.write("#### Goal F3: Minimization of stereotyping, demeaning, and erasing outputs")
    st.write("_This Goal applies to AI systems when system outputs include descriptions, depictions, or other representations of people, cultures, or society. If this Goal applies to the system, complete the table below describing the appropriate stakeholders for this intended use._")
    st.session_state['goal_f3_1'] =  st.text_input("Which stakeholder(s) will be affected?  ", value=st.session_state.get("goal_f3_1", ""))
    st.session_state['goal_f3_2'] =  st.text_area("For affected stakeholder(s) which demographic groups are you prioritizing for this Goal?  ", value=st.session_state.get("goal_f3_2", ""))
    st.session_state['goal_f3_3'] =  st.text_area("Explain how each demographic group might be affected.  ", value=st.session_state.get("goal_f3_3", ""))

    with st.expander("Goal F3 Guide"):
        with st.form("f3_guide"):
            st.write(rai_guide.f3_guide)
        
            f3_stakeholders_on = st.toggle('Generate stakeholder for me')
            f3_brainstorm = st.form_submit_button("Brainstorm Scenarios concerning stereotyping, demeaning, and erasing outputs")

            if "f3_scenarios" in st.session_state:
                st.write(st.session_state["f3_scenarios"])

            if f3_brainstorm:
                if f3_stakeholders_on:
                    res = pipeline.generate_scenarios(st, sys_info, 'f3')
                else:
                    res = pipeline.generate_scenarios(st, sys_info, 'f3', str(stakeholder_df['Stakeholders'].tolist()))
                st.write(res)
                st.session_state["f3_scenarios"] = res

