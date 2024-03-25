import streamlit as st
from menu import menu
import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import rai_guide

st.subheader("Technology readiness assessment, task complexity, role of humans, and deployment environment complexity")
st.subheader("Technology readiness assessment")
tr = int(st.session_state['technology_readiness']) if "technology_readiness" in st.session_state and st.session_state['technology_readiness'] != None else None
st.write("_Select one that best represents the system regarding this intended use._")
st.session_state['technology_readiness']=st.radio("Technology Readiness", range(len(rai_guide.technology_readiness_options)), format_func=lambda x: rai_guide.technology_readiness_options[x],index=tr)


st.subheader("Task complexity")
tc = int(st.session_state['task_complexity']) if "task_complexity" in st.session_state and st.session_state['task_complexity'] != None else None
st.write("_Select one that best represents the system regarding this intended use._")
st.session_state['task_complexity'] = st.radio("Task complexity",range(len(rai_guide.task_complexity_options)), format_func=lambda x: rai_guide.task_complexity_options[x],index=tc)


st.subheader("Role of humans")
rh = int(st.session_state['role_of_humans']) if "role_of_humans" in st.session_state and st.session_state['role_of_humans'] != None else None
st.write("_Select one that best represents the system regarding this intended use._")
st.session_state['role_of_humans'] = st.radio("Role of humans",range(len(rai_guide.role_of_humans_options)), format_func=lambda x: rai_guide.role_of_humans_options[x],index=rh)


st.subheader("Deployment environment complexity")
dec = int(st.session_state['deployment_env_complexity']) if "deployment_env_complexity" in st.session_state and st.session_state['deployment_env_complexity'] != None else None
st.write("_Select one that best represents the system regarding this intended use._")
st.session_state['deployment_env_complexity'] = st.radio("Deployment environment complexity",range(len(rai_guide.deployment_env_complexity_options)), format_func=lambda x: rai_guide.deployment_env_complexity_options[x],index=dec)

menu(st)
