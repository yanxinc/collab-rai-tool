import streamlit as st
from section1 import section1
from section2 import section2
from section6 import section6

def main():
    st.title(f"Responsible AI Impact Assessment")

    if 'num_us' not in st.session_state: st.session_state['num_us'] = 1
    if 'num_hm' not in st.session_state: st.session_state['num_hm'] = 1
    if 'num_direct_stakeholders' not in st.session_state: st.session_state['num_direct_stakeholders'] = 1
    if 'num_indirect_stakeholders' not in st.session_state: st.session_state['num_indirect_stakeholders'] = 1

    sections = {
        "Section 1: System Information": section1,
        "Section 2: Stakeholders Identification": section2,
        "Section 6: Potential harms and mitigations": section6
    }

    # Create a sidebar for page selection
    selected_section = st.sidebar.radio("Sections", list(sections.keys()))

    # Display the selected page
    if selected_section in sections:
        sections[selected_section](st)

if __name__ == "__main__":
    main()