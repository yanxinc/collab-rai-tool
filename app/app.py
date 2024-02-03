import streamlit as st
from section1 import section1
from section2 import section2
from section3 import section3
from section4 import section4
from section5 import section5


def main():
    st.title(f"Responsible AI Impact Assessment")

    st.write("For questions about specific sections within the Impact Assessment, please refer to the Impact Assessment Guide.")

    
    sections = {
        "Section 1: System Information": section1,
        "Section 2: Intended uses": section2,
        "Section 3: Adverse Impact": section3,
        "Section 4: Data Requirements": section4,
        "Section 5: Summary of Impact": section5,
    }

    # Create a sidebar for page selection
    selected_section = st.sidebar.radio("Sections", list(sections.keys()))

    # Display the selected page
    if selected_section in sections:
        sections[selected_section](st)

if __name__ == "__main__":
    main()