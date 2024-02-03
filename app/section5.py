import pandas as pd
import rai_guide as rai_guide

def section5(st):
    st.subheader("Potential harms and preliminary mitigations")
    st.write("**5.1** _Gather the potential harms you identified earlier in the Impact Assessment in this table (check the stakeholder table, fairness considerations, adverse impact section, and any other place where you may have described potential harms). Use the mitigations prompts in the Impact Assessment Guide to understand if the Responsible AI Standard can mitigate some of the harms you identified. Discuss the harms that remain unmitigated with your team and potential reviewers._")

    st.session_state['harms_and_mitigations'] = st.data_editor(st.session_state.get('harms_and_mitigations',
        pd.DataFrame(
            [
                {"Describe the potential harm": "", "Corresponding Goal from the Responsible AI Standard (if applicable)": "", "Describe your initial ideas for mitigations or explain how you might implement the corresponding Goal in the design of the system": ""},
                {"Describe the potential harm": "", "Corresponding Goal from the Responsible AI Standard (if applicable)": "", "Describe your initial ideas for mitigations or explain how you might implement the corresponding Goal in the design of the system": ""},
                {"Describe the potential harm": "", "Corresponding Goal from the Responsible AI Standard (if applicable)": "", "Describe your initial ideas for mitigations or explain how you might implement the corresponding Goal in the design of the system": ""},
                {"Describe the potential harm": "", "Corresponding Goal from the Responsible AI Standard (if applicable)": "", "Describe your initial ideas for mitigations or explain how you might implement the corresponding Goal in the design of the system": ""},
            ]
        )),  num_rows="dynamic", hide_index=True)

    st.subheader("Goal Applicability")
    st.write("**5.2** _To assess which Goals apply to this system, use the checkboxes below. When a Goal applies to only specific types of AI systems, indicate if the Goal applies to the system being evaluated in this Impact Assessment by filling the checkbox. If you indicate that a Goal does not apply to the system, explain why in the response area. If a Goal applies to the system, you must complete the requirements associated with that Goal while developing the system._")

    st.write("#### Accountability Goals")
    st.session_state["applicability_a1"] = st.checkbox("**A1: Impact assessment**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_a1", False))
    st.session_state["applicability_a2"] = st.checkbox("**A2: Oversight of significant adverse impacts**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_a2", False))
    st.session_state["applicability_a3"] = st.checkbox("**A3: Fit for purpose**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_a3", False))
    st.session_state["applicability_a4"] = st.checkbox("**A4: Data governance and management**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_a4", False))
    st.session_state["applicability_a5"] = st.checkbox("**A5: Human oversight and control**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_a5", False))
    st.session_state['reason_accountability_goal'] = st.text_input("If you selected “No” for any of the Accountability Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_accountability_goal', ""))

    st.write("#### Transparency Goals")
    st.session_state["applicability_t1"] = st.checkbox("**T1: System intelligibility for decision making**", help="Applies to: AI systems when the intended use of the generated outputs is to inform decision making by or about people.", value=st.session_state.get("applicability_t1", False))
    st.session_state["applicability_t2"] = st.checkbox("**T2: Communication to stakeholders**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_t2", False))
    st.session_state["applicability_t3"] = st.checkbox("**T3: Disclosure of AI interaction**", help="Applies to: AI systems that impersonate interactions with humans, unless it is obvious from the circumstances or context of use that an AI system is in use, and AI systems that generate or manipulate image, audio, or video content that could falsely appear to be authentic.", value=st.session_state.get("applicability_t3", False))
    st.session_state['reason_transparency_goal'] = st.text_input("If you selected “No” for any of the Transparency Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_transparency_goal', ""))

    st.write("#### Fairness Goals")
    st.session_state["applicability_f1"] = st.checkbox("**F1: Quality of service**", help="Applies to: AI systems when system users or people impacted by the system with different demographic characteristics might experience differences in quality of service that can be remedied by building the system differently.", value=st.session_state.get("applicability_f1", False))
    st.session_state["applicability_f2"] = st.checkbox("**F2: Allocation of resources and opportunities**", help="Applies to: AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare.", value=st.session_state.get("applicability_f2", False))
    st.session_state["applicability_f3"] = st.checkbox("**F3: Minimization of stereotyping, demeaning, and erasing outputs**", help="Applies to: AI systems when system outputs include descriptions, depictions, or other representations of people, cultures, or society.", value=st.session_state.get("applicability_f3", False))
    st.session_state['reason_fairness_goal'] = st.text_input("If you selected “No” for any of the Fairness Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_fairness_goal', ""))

    st.write("#### Reliability & Safety Goals")
    st.session_state["applicability_rs1"] = st.checkbox("**RS1: Reliability and safety guidance**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_rs1", False))
    st.session_state["applicability_rs2"] = st.checkbox("**RS2: Failures and remediations**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_rs2", False))
    st.session_state["applicability_rs3"] = st.checkbox("**RS3: Ongoing monitoring, feedback, and evaluation**", help="Applies to: All AI systems.", value=st.session_state.get("applicability_rs3", False))
    st.session_state['reason_reliability_safety_goal'] = st.text_input("If you selected “No” for any of the Reliability & Safety Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_reliability_safety_goal', ""))

    st.write("#### Privacy & Security Goals")
    st.session_state["applicability_ps1"] = st.checkbox("**PS1: Privacy Standard compliance**", help="Applies when the Microsoft Privacy Standard applies.", value=st.session_state.get("applicability_ps1", False))
    st.session_state["applicability_ps2"] = st.checkbox("**PS2: Security Policy compliance**", help="Applies when the Microsoft Privacy Standard applies.", value=st.session_state.get("applicability_ps2", False))
    st.session_state['reason_privacy_security_goal'] = st.text_input("If you selected “No” for any of the Privacy & Security Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_privacy_security_goal', ""))

    st.write("#### Inclusiveness Goals")
    st.session_state["applicability_i1"] = st.checkbox("**I1: Accessibility Standards compliance**", help="Applies when the Microsoft Privacy Standard applies.", value=st.session_state.get("applicability_i1", False))
    st.session_state['reason_inclusiveness_goal'] = st.text_input("If you selected “No” for any of the Inclusiveness Goals, explain why the Goal does not apply to the system.", value=st.session_state.get('reason_inclusiveness_goal', ""))
