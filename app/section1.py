import pandas as pd

def section1(st):
    st.header("Section 1: System Information")

    st.subheader("System profile")
    st.write("**1.1** _Complete the system information below._")
    st.session_state['system_name'] = st.text_input("System Name:", value=st.session_state.get("system_name", ""))
    st.session_state['team_name'] = st.text_input("Team Name:", value=st.session_state.get("team_name", ""))
    st.write("_Track revision history below._")
    st.session_state['authors'] = st.text_input("Authors:", value=st.session_state.get("authors", ""))
    st.session_state['last_updated'] = st.text_input("Last updated:", value=st.session_state.get("last_updated", ""))
    st.write("_Identify the individuals who will review your Impact Assessment when it is completed._")
    st.session_state['reviewers'] = st.text_input("Reviewers:", value=st.session_state.get("reviewers", ""))
    
    st.subheader("System lifecycle stage")
    st.write("**1.2** _Indicate the dates of planned releases for the system._")
    st.session_state['system_lifecycle'] = st.data_editor(st.session_state.get('system_lifecycle',
        pd.DataFrame(
            [
                {"Date": "", "Lifecycle stage": "Planning & analysis"},
                {"Date": "", "Lifecycle stage": "Design"},
                {"Date": "", "Lifecycle stage": "Development"},
                {"Date": "", "Lifecycle stage": "Testing"},
                {"Date": "", "Lifecycle stage": "Implementation & deployment"},
                {"Date": "", "Lifecycle stage": "Maintenance"},
                {"Date": "", "Lifecycle stage": "Retired"},
            ]
        )), hide_index=True, use_container_width=True)

    st.subheader("System description")
    st.write("**1.3** _Briefly explain, in plain language, what you're building. This will give reviewers the necessary context to understand the system and the environment in which it operates._")
    st.session_state['system_description'] = st.text_area("System description", value=st.session_state.get("system_description", ""))
    st.write("_If you have links to any supplementary information on the system such as demonstrations, functional specifications, slide decks, or system architecture diagrams, please include links below._")
    st.session_state['supplementary_info'] = st.data_editor(st.session_state.get('supplementary_info',
        pd.DataFrame(
            [
                {"Description of supplementary information": "", "Link": ""},
                {"Description of supplementary information": "", "Link": ""},
            ]
        )),  num_rows="dynamic", use_container_width=True)

    st.subheader("System purpose")
    st.write("**1.4** _Briefly describe the purpose of the system and system features, focusing on how the system will address the needs of the people who use it. Explain how the AI technology contributes to achieving these objectives._")
    st.session_state['system_purpose'] = st.text_area("System purpose", value=st.session_state.get("system_purpose", ""))

    st.subheader("System features")
    st.write("**1.5** _Focusing on the whole system, briefly describe the system features or high-level feature areas that already exist and those planned for the upcoming release._")
    st.session_state['existing_system_features'] = st.data_editor(st.session_state.get('existing_system_features',
        pd.DataFrame(
            [
                {"Existing system features": "", "System features planned for the upcoming release": ""},
                {"Existing system features": "", "System features planned for the upcoming release": ""},
                {"Existing system features": "", "System features planned for the upcoming release": ""},
                {"Existing system features": "", "System features planned for the upcoming release": ""},
            ]
        )),  num_rows="dynamic", use_container_width=True)
    st.write("_Briefly describe how this system relates to other systems or products. For example, describe if the system includes models from other systems._")
    st.session_state['relation_to_other_systems'] = st.text_input("Relation to other systems/products", value=st.session_state.get("relation_to_other_systems", ""))

    st.subheader("Geographic areas and languages")
    st.write("**1.6** _Describe the geographic areas where the system will or might be deployed to identify special considerations for language, laws, and culture._")
    st.session_state['current_deploy_location'] = st.text_input("The system is currently deployed to:", value=st.session_state.get("current_deploy_location", ""))
    st.session_state['upcoming_deploy_location'] = st.text_input("In the upcoming release, the system will be deployed to:", value=st.session_state.get("upcoming_deploy_location", ""))
    st.session_state['future_deploy_location'] = st.text_input("In the future, the system might be deployed to:", value=st.session_state.get("future_deploy_location", ""))
    st.write("_For natural language processing systems, describe supported languages:_")
    st.session_state['nlp_current_support'] = st.text_input("The system currently supports:", value=st.session_state.get("nlp_current_support", ""))
    st.session_state['nlp_upcoming_support'] = st.text_input("In the upcoming release, the system will support:", value=st.session_state.get("nlp_upcoming_support", ""))
    st.session_state['nlp_future_support'] = st.text_input("In the future, the system might support:", value=st.session_state.get("nlp_future_support", ""))

    st.subheader("Deployment mode")
    st.write("**1.7** _Document each way that this system might be deployed._")
    st.session_state['current_deployment'] = st.text_input("How is the system currently deployed?:", value=st.session_state.get("current_deployment", ""))
    st.session_state['deployement_change'] = st.text_input("Will the deployment mode change in the upcoming release?If so, how?:", value=st.session_state.get("deployement_change", ""))

    st.subheader("Intended uses")
    st.write("**1.8** _Intended uses are the uses of the system your team is designing and testing for. An intended use is a description of who will use the system, for what task or purpose, and where they are when using the system. They are not the same as system features, as any number of features could be part of an intended use. Fill in the table with a description of the system's intended use(s)._")
    st.session_state['intended_uses'] = st.data_editor(st.session_state.get('intended_uses',
        pd.DataFrame(
            [
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
            ]
        )),  num_rows="dynamic", hide_index=False, use_container_width=True)