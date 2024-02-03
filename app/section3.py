import rai_guide as rai_guide

# import os
# import openai
# from cred import KEY

# gpt_model = "gpt-3.5-turbo"
# gpt_model = "gpt-4-0613"

# openai.api_key = KEY

# messages = [ {"role": "system", "content": "You are an intelligent assistant with a specialization in Responsible AI Impact Assessment. Keep your responses specific to the system I describe."} ]

def section3(st):
    # sys_info = f"I am building a {st.session_state.get('system_name', '__')} application. {st.session_state.get('system_description', '__')}. {st.session_state.get('system_purpose', '__')}. The system is currently deployed to: {st.session_state.get('current_deploy_location', 'United States')}"
    # messages.append({'role': 'user', 'content': sys_info})


    with st.expander("Thinking through adverse impact"):
        st.write("#### Guidance")
        st.write("Even the best systems have limitations, fail sometimes, and can be misused. Consider known limitations of the system, the potential impact of failure on stakeholders, and the potential impact of misuse.")
        st.write("#### Prompts")
        st.write("- Try thinking from a hacker's perspective.\n- Consider what a non-expert might assume about the system.\n- Imagine a very negative news story about the system. What does it say?")

    st.subheader("Restricted Uses")
    st.write("**3.1** _If any uses of the system are subject to a legal or internal policy restriction, list them here, and follow the requirements for those uses._")
    st.session_state['restricted_uses'] = st.text_area("Restricted Uses", value=st.session_state.get("restricted_uses", ""))

    # with st.expander("Restricted Uses Guide"):
    #     button_3_1 = st.button("Brainstorm Restricted Uses")
    #     if button_3_1:
    #         response = openai.ChatCompletion.create(
    #             model=gpt_model, 
    #             messages=messages + [{"role": "user", "content": f"Brainstorm and list any uses of the system are subject to a legal or internal policy restriction. Give examples from existing similar systems. "}] 
    #         ) 
    #         st.write(response['choices'][0]['message']['content'])

    st.subheader("Unsupported uses")
    st.write("**3.2** _Uses for which the system was not designed or evaluated or that should be avoided._")
    st.session_state['unsupported_uses'] = st.text_area("Unsupported uses", value=st.session_state.get("unsupported_uses", ""))

    with st.expander("Unsupported uses Guide"):
        st.write(rai_guide.unsupported_uses_guide)
        st.write("**Examples:**")
        st.write(rai_guide.unsupported_uses_examples)
    #     button_3_2 = st.button("Brainstorm Unsupported uses")
    #     if button_3_2:
    #         response = openai.ChatCompletion.create(
    #             model=gpt_model, 
    #             messages=messages + [{"role": "user", "content": f"{rai_guide.unsupported_uses_guide}. Brainstorm some uses for which the system was not designed or evaluated or that should be avoided"}] 
    #         ) 
    #         st.write(response['choices'][0]['message']['content'])


    st.subheader("Known limitations")
    st.write("**3.3** _Describe the known limitations of the system. This could include scenarios where the system will not perform well, environmental factors to consider, or other operating factors to be aware of._")
    st.session_state['known_limitations'] = st.text_area("Known limitations",value=st.session_state.get("known_limitations", ""))

    with st.expander("Known limitations Guide"):
        st.write(rai_guide.known_limitations_guide)
        st.write("**Examples:**")
        st.write(rai_guide.known_limitations_examples)
        st.write("**Prompts:**")
        st.write(rai_guide.known_limitations_prompts)
        # button_3_3 = st.button("Brainstorm Known limitations")
        # if button_3_3:
        #     response = openai.ChatCompletion.create(
        #         model=gpt_model, 
        #         messages=messages + [{"role": "user", "content": f"Describe the known limitations of the system. This could include scenarios where the system will not perform well, environmental factors to consider, or other operating factors to be aware of. {rai_guide.known_limitations_prompts}"}] 
        #     ) 
        #     st.write(response['choices'][0]['message']['content'])

    st.subheader("Potential impact of failure on stakeholders")
    st.write("**3.4** _Define predictable failures, including false positive and false negative results for the system as a whole and how they would impact stakeholders for each intended use._")
    st.session_state['potential_failure_impact'] = st.text_area("Potential impact of failure on stakeholders",value=st.session_state.get("potential_failure_impact", ""))

    with st.expander("Potential impact of failure on stakeholders Guide"):
        st.write(rai_guide.failure_impact_guide)
        st.write("**Prompts:**")
        st.write(rai_guide.failure_impact_prompts)
        # button_3_4 = st.button("Brainstorm Potential impact of failure on stakeholders")
        # if button_3_4:
        #     response = openai.ChatCompletion.create(
        #         model=gpt_model, 
        #         messages=messages + [{"role": "user", "content": f"{rai_guide.failure_impact_guide} Consider: {rai_guide.failure_impact_prompts}"}] 
        #     ) 
        #     st.write(response['choices'][0]['message']['content'])

    st.subheader("Potential impact of misuse on stakeholders")
    st.write("**3.5** _Define system misuse, whether intentional or unintentional, and how misuse could negatively impact each stakeholder. Identify and document whether the consequences of misuse differ for marginalized groups. When serious impacts of misuse are identified, note them in the summary of impact as a potential harm._")
    st.session_state['potential_misuse_impact'] = st.text_area("Potential impact of misuse on stakeholders",value=st.session_state.get("potential_misuse_impact", ""))

    with st.expander("Potential impact of misuse on stakeholders Guide"):
        st.write(rai_guide.misuse_impact_guide)
        st.write("**Prompts:**")
        st.write(rai_guide.misuse_impact_prompts)
        # button_3_5 = st.button("Brainstorm Potential impact of misuse on stakeholders")
        # if button_3_5:
        #     response = openai.ChatCompletion.create(
        #         model=gpt_model, 
        #         messages=messages + [{"role": "user", "content": f"Define system misuse, whether intentional or unintentional, and how misuse could negatively impact each stakeholder. Identify and document whether the consequences of misuse differ for marginalized groups. When serious impacts of misuse are identified, note them in the summary of impact as a potential harm. Consider: {rai_guide.misuse_impact_prompts}"}] 
        #     ) 
        #     st.write(response['choices'][0]['message']['content'])

    st.subheader("Sensitive Uses")
    st.write("**3.6** _Consider whether the use or misuse of the system could meet any of the Microsoft Sensitive Use triggers below._")
    st.session_state['sensitive_use1'] = st.checkbox("**Consequential impact on legal position or life opportunities**", help="The use or misuse of the AI system could affect an individual's: legal status, legal rights, access to credit, education, employment, healthcare, housing, insurance, and social welfare benefits, services, or opportunities, or the terms on which they are provided.", value=st.session_state.get("sensitive_use1", False))
    st.session_state['sensitive_use2'] = st.checkbox("**Risk of physical or psychological injury**", help="The use or misuse of the AI system could result in significant physical or psychological injury to an individual.",value=st.session_state.get("sensitive_use2", False))
    st.session_state['sensitive_use3'] = st.checkbox("**Threat to human rights**", help="The use or misuse of the AI system could restrict, infringe upon, or undermine the ability to realize an individual's human rights. Because human rights are interdependent and interrelated, AI can affect nearly every internationally recognized human right.",value=st.session_state.get("sensitive_use3", False))
