import streamlit as st
from menu import menu

def main():
    st.title(f"Responsible AI Impact Assessment (User Testing Version)")

    if 'num_us' not in st.session_state: st.session_state['num_us'] = 1
    if 'num_hm' not in st.session_state: st.session_state['num_hm'] = 1
    if 'num_direct_stakeholders' not in st.session_state: st.session_state['num_direct_stakeholders'] = 1
    if 'num_indirect_stakeholders' not in st.session_state: st.session_state['num_indirect_stakeholders'] = 1
    
    menu(st)
    
if __name__ == "__main__":
    main()