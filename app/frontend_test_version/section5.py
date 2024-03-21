import os, sys
app_dir = os.path.dirname(os.path.dirname(__file__))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import time

def section5(st):
    st.subheader("Fairness Considerations")

    st.write("For the following Fairness Goal, \n1) Select the relevant stakeholder(s) (e.g., system user, person impacted by the system); \n2) Consider potential AI related harms and consequences that may arise from the system; and \n3) Describe your ideas for mitigations.")

    st.write("#### Goal F3: Minimization of stereotyping, demeaning, and erasing outputs")

    st.write(f"_This Goal applies to AI systems when system outputs include descriptions, depictions, or other representations of people, cultures, or society. Consider: {rai_guide.f3_guide}_")

    st.markdown("_When considering this fairness goal, think about different demographic group of stakeholders and consider marginalized groups._", help="**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.\n\n**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.")


    all_stakeholders = helper.get_stakeholders(st)

    f_enum = helper.Task.F3.value

    sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"

    if all_stakeholders != [] and f'{f_enum}_task_status' not in st.session_state:
        helper.send_req(st, sys_info, f_enum, all_stakeholders)
        print("sending request for f3")

    st.session_state['f3_selected_stakeholders'] = st.multiselect(
        'Which stakeholders will be affected?',
        all_stakeholders,
        st.session_state.get('f3_selected_stakeholders', [])
    )

    f3_brainstorm = st.button("Help me brainstorm scenarios concerning Minimization of stereotyping, demeaning, and erasing outputs", use_container_width=True)

    if f'f3_clicked' in st.session_state and f'{f_enum}_result' in st.session_state:
        st.write(st.session_state[f'{f_enum}_result'])

    if f3_brainstorm:
        if all_stakeholders != []:
            st.session_state[f'f3_clicked'] = True
            if f'{f_enum}_task_status' in st.session_state:
                if st.session_state[f'{f_enum}_task_status'] == 'Running':
                    with st.spinner('Generating Scenarios...'):
                        while True:
                            result = helper.poll_task_status(st, st.session_state[f'{f_enum}_task_id'], helper.Task.F3.value)
                            if result:
                                st.write(result)
                                st.session_state[f"{f_enum}_result"] = result
                                break
                            else:
                                time.sleep(10)
        else:
            st.write("Please fill in stakeholders first")

    st.write("For each identified stakeholder, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.")
    st.session_state[f'goal_f3_2'] =  st.text_area("Describe any potential harms  ", value=st.session_state.get(f"goal_f3_2", ""))

    st.write("After identifying potential harms, propose practical strategies to mitigate these issues. Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness. List the actions you might take to mitigate the potential harms and fairness issues you have identified.")
    st.markdown("Examples of mitigation strategies for 'Minimization of stereotyping, demeaning, and erasing outputs' realted harms include developing a rigorous understanding of how different demographic groups are represented within the AI system and modifying the system to minimize harmful outputs.", help="For example, an image search system that predominantly returns images of men in response to the query “chief executive officer” may underrepresent non-male chief executive officers. To mitigate this, the system can be modified to provide more representative outputs.")
    st.session_state[f'goal_f3_3'] =  st.text_area("Describe your ideas for mitigations  ", value=st.session_state.get(f"goal_f3_3", ""))

    