import pandas as pd

def section1(st):
    st.header("Section 1: System Information")

    st.session_state['system_name'] = st.text_input("**System Name:**", value=st.session_state.get("system_name", ""))
    
    st.session_state['system_description'] = st.text_area("**System description:** _Briefly explain, in plain language, what you're building. This will give reviewers the necessary context to understand the system and the environment in which it operates._", value=st.session_state.get("system_description", ""))
    
    st.session_state['system_purpose'] = st.text_area("**System purpose:** _Briefly describe the purpose of the system and system features, focusing on how the system will address the needs of the people who use it. Explain how the AI technology contributes to achieving these objectives._", value=st.session_state.get("system_purpose", ""))

    st.subheader("Intended uses")
    st.write("_Intended uses are the uses of the system your team is designing and testing for. An intended use is a description of who will use the system, for what task or purpose, and where they are when using the system. They are not the same as system features, as any number of features could be part of an intended use. Fill in the table with a description of the system's intended use(s)._")

    
    for i in range(st.session_state['num_iu']):
        st.write(f"**Intended use #{i+1}**")
        st.session_state[f'iu{i+1}'] = st.text_input(f"Intended Use {i+1} Name", value=st.session_state.get(f"iu{i+1}", ""))
        st.session_state[f'iu{i+1}_des'] = st.text_input(f"Intended Use {i+1} Description", value=st.session_state.get(f"iu{i+1}_des", ""))

    add_iu_button = st.button("Add Intended Use")
    if add_iu_button:
        st.session_state['num_iu'] += 1
    