import pandas as pd

def section1(st):
    st.header("Section 1: System Information")

    st.write("In this section, you will provide information about your system. This foundational data is critical for understanding the operational context and purpose of your system, which will enable a more thorough and responsible assessment of its impact. Please follow the instructions below to complete this section.")

    st.session_state['system_name'] = st.text_input("**System Name:**", value=st.session_state.get("system_name", ""))
    
    st.session_state['system_description'] = st.text_area("**System description:** _Please provide a brief overview of the system you are building. Describe in simple terms and try to avoid jargon or technical terms._", value=st.session_state.get("system_description", ""), help="Consider: \n- What are you building? \n- What does it do? \n - How does it work?")
    
    st.session_state['system_purpose'] = st.text_area("""**System purpose:** _Please briefly describe the purpose of the system and system features, focusing on how the system will address the needs of the people who use it. Explain how the AI technology contributes to achieving these objectives_""", value=st.session_state.get("system_purpose", ""), help="**Focus on the why**.\nThis statement should include:\n1. the end user or primary customer of the system,\n2. how they complete this task today, or their current situation,\n3. the value that the system is intended to deliver,\n4. how it improves on today's situation.")

    st.subheader("User stories")
    st.markdown("_User Stories describe the uses of the system from the perspective of an end user. It typically follows the format of: 'As a [role], I want [function], so that [value]'. Please describe at least 1-2 use cases. The following sections will be completed based on your primary User Story that should involve some notion of AI usage._", help="Example User Story:\n\nAs a *product manager*, \n\nI want *an AI-powered feature that can automatically categorize customer feedback into actionable insights*,\n\n so that *we can more efficiently identify and prioritize improvements to our product, enhancing user satisfaction and engagement*.")
    
    for i in range(st.session_state['num_us']):
        st.write(f"**User Stories #{i+1}**")
        st.session_state[f'us{i+1}_des'] = st.text_area(f"User Story {i+1} Description", value=st.session_state.get(f"us{i+1}_des", ""))

    add_us_button = st.button("Add More User Story")
    if add_us_button:
        st.session_state['num_us'] += 1
    