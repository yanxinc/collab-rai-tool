import rai_guide as rai_guide

def section4(st):
    st.subheader("Data Requirements")
    st.write("**4.1** _Define and document data requirements with respect to the system's intended uses, stakeholders, and the geographic areas where the system will be deployed._")
    st.session_state['data_requirements'] = st.text_area("Data Requirements",value=st.session_state.get("data_requirements", ""))

    st.subheader("Existing data sets")
    st.write("**4.2** _If you plan to use existing data sets to train the system, assess the quantity and suitability of available data sets that will be needed by the system in relation to the data requirements defined above. If you do not plan to use pre-defined data sets, enter “N/A” in the response area._")
    st.session_state['existing_datasets'] = st.text_input("Existing data sets",value=st.session_state.get("existing_datasets", ""))
