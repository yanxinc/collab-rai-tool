def menu(st):
    # set container background color
    st.markdown(
"""
    <style>
    .st-emotion-cache-r421ms {
        background-color: #fbfaf5;
        color: black;
    } 
    </style>
""", unsafe_allow_html=True)

    st.sidebar.page_link("pages/section1.py", label="Section 1: System Information")

    display_stakeholder = 'us1_des' in st.session_state and st.session_state['us1_des'] != ""
    st.sidebar.page_link("pages/section2.py", label="Section 2: Stakeholders Identification", disabled=not display_stakeholder),

    if 'can_display_fairness_sections' not in st.session_state: st.session_state['can_display_fairness_sections'] = False
    dispaly_fairness_goals = st.session_state['can_display_fairness_sections']
    st.sidebar.page_link("pages/section3.py", label="Section 3: Fairness Goal 1 - Quality of service", disabled=not dispaly_fairness_goals),
    st.sidebar.page_link("pages/section4.py", label="Section 4: Fairness Goal 2 - Allocation of resources and opportunities", disabled=not dispaly_fairness_goals),
    st.sidebar.page_link("pages/section5.py", label="Section 5: Fairness Goal 3 - Minimization of stereotyping, demeaning, and erasing outputs", disabled=not dispaly_fairness_goals),


    display_section6 = 'goal_f3_2' in st.session_state and st.session_state['goal_f3_2'] != "" and 'goal_f3_3' in st.session_state and st.session_state['goal_f3_3'] != ""
    st.sidebar.page_link("pages/section6.py", label="Section 6: Potential harms and mitigations", disabled=not display_section6),