import pandas as pd

def section1(st):
    st.header("Section 1: System Information")

    st.session_state['system_name'] = st.text_input("**System Name:**", value=st.session_state.get("system_name", ""))
    
    st.session_state['system_description'] = st.text_area("**System description:** _Briefly explain, in plain language, what you're building. This will give reviewers the necessary context to understand the system and the environment in which it operates._", value=st.session_state.get("system_description", ""))
    
    st.session_state['system_purpose'] = st.text_area("**System purpose:** _Briefly describe the purpose of the system and system features, focusing on how the system will address the needs of the people who use it. Explain how the AI technology contributes to achieving these objectives._", value=st.session_state.get("system_purpose", ""))

    st.write("**Intended uses:** _Intended uses are the uses of the system your team is designing and testing for. An intended use is a description of who will use the system, for what task or purpose, and where they are when using the system. They are not the same as system features, as any number of features could be part of an intended use. Fill in the table with a description of the system's intended use(s)._")
    intended_uses_df = st.data_editor(
        pd.DataFrame(
            [
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
                {"Name of intended use(s)": "", "Description of intended use(s)": ""},
            ]
        ),  num_rows="dynamic", hide_index=False, use_container_width=True)
    
    return intended_uses_df