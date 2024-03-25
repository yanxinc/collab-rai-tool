import streamlit as st
from menu import menu

def main():
    st.title(f"Responsible AI Impact Assessment (User Testing Version)")

    if 'num_us' not in st.session_state: st.session_state['num_us'] = 1
    if 'num_hm' not in st.session_state: st.session_state['num_hm'] = 1
    if 'num_direct_stakeholders' not in st.session_state: st.session_state['num_direct_stakeholders'] = 1
    if 'num_indirect_stakeholders' not in st.session_state: st.session_state['num_indirect_stakeholders'] = 1
    
    st.write("This is a user testing version of the Responsible AI Impact Assessment tool. The purpose of this tool is to help you think through the potential impacts of an AI system you are developing. The tool is divided into sections, each focusing on a different aspect of the system. Please follow the instructions in each section to complete the assessment. Your feedback is valuable and will help improve the tool. Thank you for participating in this user test!")

    with st.expander('Please complete the following sections with a AI/ML realted system that you have worked on or are familiar with.'):
        st.write(" If you do not have a system in mind, you can use the 'Prefill with Movie Scenario' button below to populate the fields with a movie recommendation system scenario.")

        if st.button("Prefill with Movie Scenario"):
            st.session_state['system_name'] = "Movie Recommendation System"
            st.session_state['system_description'] = "A system that provides movie recommendations to users based on their watching history and ratings data. The system can receive recommendation requests and needs to reply with a list of recommended movies. "
            st.session_state['system_purpose'] = "The purpose of this system is to suggest movies to users to allow for better user experience. The users (movie watchers) would be able to receive more personalized recommendations. The AI / ML model uses collaborative filtering algorithms to accumulate and learn from users' past evaluations of movies to approximate ratings of unrated movies and then give recommendations based on these estimates."
            st.session_state[f'us1_des'] = "As a movie watcher, I want to request for personalized recommendations based on my interest and previous watch history, so that I can discover new films that match my preferences and enhance my viewing experience."

    _, col2 = st.columns([0.7,0.3])
    with col2:
        if st.button('Begin Study', use_container_width=True):
            st.switch_page("pages/section1.py")

    menu(st)
    
if __name__ == "__main__":
    main()