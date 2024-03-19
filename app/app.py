import streamlit as st
from section1 import section1
from section2 import section2
from section3 import section3
import re

def main():
    st.title(f"Responsible AI Impact Assessment")

    if 'num_us' not in st.session_state: st.session_state['num_us'] = 1
    if 'num_hm' not in st.session_state: st.session_state['num_hm'] = 1

    if 'sections' not in st.session_state: st.session_state['sections'] = {
        "Section 1: System Information": section1,
    }
        
    for i in range(1,st.session_state['num_us']+1):
        st.session_state['sections'][f"Section 2.{i}: User Story {i}"] = section2

    st.session_state['sections']["Section 3: Potential harms and mitigations"] = section3

    # Create a sidebar for page selection
    selected_section = st.sidebar.radio("Sections", list(st.session_state['sections'].keys()))

    # Display the selected page
    if selected_section in st.session_state['sections']:
        match = re.search(r'Section 2\.(\d+):', selected_section)
        if match:
            i = match.group(1)
            section2(st, i)
        else:
            st.session_state['sections'][selected_section](st)


if __name__ == "__main__":
    main()