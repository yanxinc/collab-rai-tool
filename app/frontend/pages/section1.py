import streamlit as st
from menu import menu

# st.set_page_config(layout="centered",initial_sidebar_state="collapsed")

st.header("Section 1: System Information")

st.write("In this section, you will provide information about your system. This foundational data is critical for understanding the operational context and purpose of your system, which will enable a more thorough and responsible assessment of its impact. Please follow the instructions below to complete this section.")


with st.expander("If you already have all your system information, you can paste it here, skip this section and go to the next page."):
    st.session_state['all_system_info'] = st.text_area("""System information""", value=st.session_state.get("all_system_info", ""),height=200)

    c1, c2 = st.columns([0.7,0.3])

    with c2:
        if st.button('Go Directly to Next Page', use_container_width=True):
            if 'all_system_info' in st.session_state and st.session_state['all_system_info'] != "":
                st.switch_page("pages/section2.py")
            else:
                st.toast("Please fill in your system information first")

st.session_state['system_description'] = st.text_area("**System description:** Please provide a brief overview of the system you are building in 2-3 sentences. Describe in simple terms and try to avoid jargon or technical terms.", value=st.session_state.get("system_description", ""), help="Consider: \n- What are you building? \n- What does it do? \n - How does it work?")

st.session_state['system_purpose'] = st.text_area("""**System purpose:** Please briefly describe the purpose of the system and system features, focusing on how the system will address the needs of the people who use it. Explain how the AI technology contributes to achieving these objectives""", value=st.session_state.get("system_purpose", ""), help="Focus on the why.\nThis statement should include:\n1. the end user or primary customer of the system,\n2. how they complete this task today, or their current situation,\n3. the value that the system is intended to deliver,\n4. how it improves on today's situation.")

st.subheader("User stories")
st.markdown(":closed_book: **Definition:** User Stories describe the uses of the system from the perspective of an end user. It typically follows the format of: 'As a [role], I want [function], so that [value]'.", help="Example User Story:\n\nAs a *product manager*, \n\nI want *an AI-powered feature that can automatically categorize customer feedback into actionable insights*,\n\n so that *we can more efficiently identify and prioritize improvements to our product, enhancing user satisfaction and engagement*.")

st.session_state[f'us1_des'] = st.text_area(":lower_left_ballpoint_pen: **Instruction:** Please describe 1 primary use case of your system that involves some notion of AI usage.", value=st.session_state.get(f"us1_des", ""))

col1, col2 = st.columns([0.7,0.3])
with col2:
    if st.button('Next Page', use_container_width=True):
        if 'us1_des' in st.session_state and st.session_state['us1_des'] != "":
            st.switch_page("pages/section2.py")
        else:
            st.toast("Please fill in an user story first")

menu(st)
