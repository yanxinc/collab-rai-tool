import pandas as pd
import rai_guide as rai_guide
import pipeline as pipeline

def section2(st):
    intended_use1 = st.session_state['intended_uses'].iloc[0]["Name of intended use(s)"].strip()
    intended_use1_description = st.session_state['intended_uses'].iloc[0]["Description of intended use(s)"]

    sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An intended use is {intended_use1}. The description of this indented use is {intended_use1_description}"
    
    st.write(f"Intended use #1 : **{intended_use1 if intended_use1 != '' else '[Name of intended use]'}** - repeat for each intended use")
    st.write("Copy and paste the Intended Use #1 section and repeat questions 2.1 - 2.8 for each intended use you identified above.")

    st.subheader("Assessment of fitness for purpose")
    st.write("**2.1** _Assess how the system's use will solve the problem posed by each intended use, recognizing that there may be multiple valid ways in which to solve the problem._")
    st.session_state['purpose_fitness'] = st.text_area("Assessment of fitness for purpose",value=st.session_state.get("purpose_fitness", ""))

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


    st.subheader("Stakeholders for Goal-driven requirements from the Responsible AI Standard")
    st.write("**2.3** _Certain Goals in the Responsible AI Standard require you to identify specific types of stakeholders. You may have included them in the stakeholder table above. For the Goals below that apply to the system, identify the specific stakeholder(s) for this intended use. If a Goal does not apply to the system, enter “N/A” in the table._")

    st.write("#### Goal A5: Human oversight and control")
    st.write("_This Goal applies to all AI systems._")
    st.session_state['goal_a5_1'] =  st.text_input("Who is responsible for troubleshooting, managing, operating, overseeing, and controlling the system during and after deployment?", value=st.session_state.get("goal_a5_1", ""))
    st.session_state['goal_a5_2'] =  st.text_area("For these stakeholders, identify their oversight and control responsibilities.", value=st.session_state.get("goal_a5_2", ""))

    with st.expander("Goal A5 Guide"):
        st.write(rai_guide.a5_guide)
        st.write(rai_guide.a5_2)
        st.write(rai_guide.a5_4)


    st.write("#### Goal T1: System intelligibility for decision making")
    st.write("_This Goal applies to AI systems when the intended use of the generated outputs is to inform decision making by or about people. If this Goal applies to the system, complete the questions below._")
    st.session_state['goal_t1_1'] =  st.text_input("Who will use the outputs of the system to make decisions?", value=st.session_state.get("goal_t1_1", ""))
    st.session_state['goal_t1_2'] =  st.text_input("Who will decisions be made about?", value=st.session_state.get("goal_t1_2", ""))
    with st.expander("Goal T1 Guide"):
        st.write(rai_guide.t1_guide)
        st.write(rai_guide.t1_1)
        st.write(rai_guide.t1_2)


    st.write("#### Goal T2: Communication to stakeholders")
    st.write("_This Goal applies to all AI systems._")
    st.session_state['goal_t2_1'] =  st.text_input("Who will make decisions about whether to employ the system for particular tasks?", value=st.session_state.get("goal_t2_1", ""))
    st.session_state['goal_t2_2'] =  st.text_input("Who develops or deploys systems that integrate with this system?", value=st.session_state.get("goal_t2_2", ""))
    with st.expander("Goal T2 Guide"):
        st.write(rai_guide.t2_guide)
        st.write(rai_guide.t2_1)

    st.write("#### Goal T3: Disclosure of AI interaction")
    st.write("_This Goal applies to AI systems that impersonate interactions with humans, unless it is obvious from the circumstances or context of use that an AI system is in use, and AI systems that generate or manipulate image, audio, or video content that could falsely appear to be authentic. If this Goal applies to the system, complete the question below._")
    st.session_state['goal_t3'] =  st.text_input("Who will use or be exposed to the system?", value=st.session_state.get("goal_t3", ""))
    with st.expander("Goal T3 Guide"):
        st.write(rai_guide.t2_guide)

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


    st.subheader("Technology readiness assessment")
    tr = int(st.session_state['technology_readiness']) if "technology_readiness" in st.session_state and st.session_state['technology_readiness'] != None else None
    st.write("**2.5** _Select one that best represents the system regarding this intended use._")
    st.session_state['technology_readiness']=st.radio("Technology Readiness", range(len(rai_guide.technology_readiness_options)), format_func=lambda x: rai_guide.technology_readiness_options[x],index=tr)


    st.subheader("Task complexity")
    tc = int(st.session_state['task_complexity']) if "task_complexity" in st.session_state and st.session_state['task_complexity'] != None else None
    st.write("**2.6** _Select one that best represents the system regarding this intended use._")
    st.session_state['task_complexity'] = st.radio("Task complexity",range(len(rai_guide.task_complexity_options)), format_func=lambda x: rai_guide.task_complexity_options[x],index=tc)


    st.subheader("Role of humans")
    rh = int(st.session_state['role_of_humans']) if "role_of_humans" in st.session_state and st.session_state['role_of_humans'] != None else None
    st.write("**2.7** _Select one that best represents the system regarding this intended use._")
    st.session_state['role_of_humans'] = st.radio("Role of humans",range(len(rai_guide.role_of_humans_options)), format_func=lambda x: rai_guide.role_of_humans_options[x],index=rh)


    st.subheader("Deployment environment complexity")
    dec = int(st.session_state['deployment_env_complexity']) if "deployment_env_complexity" in st.session_state and st.session_state['deployment_env_complexity'] != None else None
    st.write("**2.8** _Select one that best represents the system regarding this intended use._")
    st.session_state['deployment_env_complexity'] = st.radio("Deployment environment complexity",range(len(rai_guide.deployment_env_complexity_options)), format_func=lambda x: rai_guide.deployment_env_complexity_options[x],index=dec)
