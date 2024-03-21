import rai_guide as rai_guide

def section6(st):
    if "sh_direct_1" in st.session_state:
        st.write(st.session_state["sh_direct_1"])

    st.subheader("Potential harms and preliminary mitigations")
    st.write("_Gather the potential harms you identified earlier in the Impact Assessment in this table (check the stakeholder table, fairness considerations, adverse impact section, and any other place where you may have described potential harms). Use the mitigations prompts in the Impact Assessment Guide to understand if the Responsible AI Standard can mitigate some of the harms you identified. Discuss the harms that remain unmitigated with your team and potential reviewers._")

    for i in range(st.session_state['num_hm']):
        st.write(f"**Harm & Mitigation #{i+1}**")
        st.session_state[f'h{i+1}'] = st.text_input(f"{i+1}. Describe the potential harm", value=st.session_state.get(f"h{i+1}", ""))
        st.session_state[f'm{i+1}'] = st.text_area(f"{i+1}. Describe your ideas for mitigations", value=st.session_state.get(f"m{i+1}", ""))

    add_hm_button = st.button("Add More")
    if add_hm_button:
        st.session_state['num_hm'] += 1

    st.write("_This is only a portion of a complete Responsible AI Impact Assessment. Note that there are more questions, but excluded here._")