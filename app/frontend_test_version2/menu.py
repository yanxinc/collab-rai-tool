def menu(st):
    # set container background color
    st.markdown(
"""
    <style>
    .st-emotion-cache-r421ms {
        background-color: #fbfaf5;
        color: black;
    } 
    .st-emotion-cache-l9bjmx p {
        word-break: break-word;
        margin-bottom: 0px;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

    study_started = 'study_started' in st.session_state and st.session_state['study_started']
    st.sidebar.page_link("pages/section1.py", label="Section 1: System Information", disabled=not study_started)

    display_stakeholder = study_started and ('us1_des' in st.session_state and st.session_state['us1_des'] != "") or ('all_system_info' in st.session_state and st.session_state['all_system_info'] != "")
    st.sidebar.page_link("pages/section2.py", label="Section 2: Stakeholders Identification", disabled=not display_stakeholder),

    if 'can_display_fairness_sections' not in st.session_state: st.session_state['can_display_fairness_sections'] = False
    dispaly_fairness_goals = st.session_state['can_display_fairness_sections']
    st.sidebar.page_link("pages/section5.py", label="Section 3: Minimization of stereotyping, demeaning, and erasing outputs", disabled=not dispaly_fairness_goals),
    st.sidebar.page_link("pages/section4.py", label="Section 4: Allocation of resources and opportunities", disabled=not dispaly_fairness_goals),
    
    
    st.sidebar.page_link("pages/section3.py", label="Section 5: Quality of service", disabled=True),
    st.sidebar.page_link("pages/section6.py", label="Section 6: Potential harms and mitigations", disabled=True),
    st.sidebar.page_link("pages/section7.py", label="Section 7: Technology readiness assessment, task complexity, role of humans, and deployment environment complexity", disabled=True),
    st.sidebar.page_link("pages/section8.py", label="Section 8: Adverse Impact", disabled=True),
    st.sidebar.page_link("pages/section9.py", label="Section 9: Data Requirements", disabled=True),