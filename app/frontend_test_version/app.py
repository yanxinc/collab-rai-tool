import streamlit as st
from section1 import section1
from section2 import section2
from section3 import section3
from section4 import section4
from section5 import section5
from section6 import section6

def main():
    st.title(f"Responsible AI Impact Assessment (User Testing Version)")

    if 'num_us' not in st.session_state: st.session_state['num_us'] = 1
    if 'num_hm' not in st.session_state: st.session_state['num_hm'] = 1
    if 'num_direct_stakeholders' not in st.session_state: st.session_state['num_direct_stakeholders'] = 1
    if 'num_indirect_stakeholders' not in st.session_state: st.session_state['num_indirect_stakeholders'] = 1

    sections = {
        "Section 1: System Information": section1,
        "Section 2: Stakeholders Identification": section2,
        "Section 3: Fairness Goal 1 - Quality of service": section3,
        "Section 4: Fairness Goal 2 - Allocation of resources and opportunities": section4,
        "Section 5: Fairness Goal 3 - Minimization of stereotyping, demeaning, and erasing outputs": section5,
        "Section 6: Potential harms and mitigations": section6
    }

    # Create a sidebar for page selection
    selected_section = st.sidebar.radio("Sections", list(sections.keys()))

    # Display the selected page
    if selected_section in sections:
        sections[selected_section](st)

if __name__ == "__main__":
    main()