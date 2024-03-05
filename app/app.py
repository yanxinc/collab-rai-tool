import streamlit as st
from section1 import section1
from section2 import section2

def main():
    st.title(f"Responsible AI Impact Assessment")

    st.write("For questions about specific sections within the Impact Assessment, please refer to the Impact Assessment Guide.")

    intended_uses_df = section1(st)
    section2(st, intended_uses_df)
    

if __name__ == "__main__":
    main()