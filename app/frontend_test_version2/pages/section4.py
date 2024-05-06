import os, sys
app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
import helper, rai_guide
import streamlit as st
from menu import menu
import json
from streamlit_feedback import streamlit_feedback

st.set_page_config(layout="wide",initial_sidebar_state="expanded")

def write_scenarios(f_enum):
    scenario_heading_list = st.session_state[f'{f_enum}_result']
    for i in range(len(scenario_heading_list)):
        c1, c2 = st.columns([0.7,0.3])
        with c1:
            st.write(helper.format_scenario_result(scenario_heading_list[i], i))
            
        with c2:
            streamlit_feedback(feedback_type="thumbs", key=f's{i}_thumbs', optional_text_label='Optional explanation')

    st.write(":red[Note: The generated scenarios are only examples of potential harms and fairness issues that could arise from the system's deployment and use. They are potential starting points for considering the fairness implications of the system. We cannot guarantee the accuracy and completeness of the information provided. Please think beyond the generated sceanrios and do not limit your brainstorming of harms to these scenarios.]")

def display_buttons():
    c3, c4 = st.columns([0.5,0.5])
    with c3:
        if f'{f_enum}_result_unpicked' not in st.session_state:
            more_scenarios_btn = st.button("Show more scenarios", key=f"{f_enum}_more_scenarios",use_container_width=True)
            if more_scenarios_btn:
                result = helper.more_scenarios(st, st.session_state[f'{f_enum}_task_id'], f_enum)
                if result:
                    st.write(result)
                    st.session_state[f"{f_enum}_result_unpicked"] = result
                    st.session_state[f"{f_enum}_result"] = st.session_state[f"{f_enum}_result"] + result
                    st.rerun()
    with c4:
        if f'{f_enum}_result' in st.session_state:
            regenerate_btn = st.button("🔄 Regenerate Scenarios", key=f"{f_enum}_regenerate_btn",use_container_width=True)

            if regenerate_btn:
                feedback = ""
                for i in range(len(st.session_state[f'{f_enum}_result'])):
                    if st.session_state[f's{i}_thumbs'] and st.session_state[f's{i}_thumbs']['score'] == '👎':
                        feedback += st.session_state[f's{i}_thumbs']['text']
                    del st.session_state[f's{i}_thumbs']

                del st.session_state[f'{f_enum}_result']
                if f'{f_enum}_result_unpicked' in st.session_state:
                    del st.session_state[f'{f_enum}_result_unpicked']

                helper.send_req(st, sys_info, f_enum, all_stakeholders, feedback)
                print(f"sending regenerate request for f3 with feedback: {feedback}")
                helper.wait_response(st, f_enum)
                st.rerun()

st.subheader("Fairness Considerations - Allocation of resources and opportunities")

st.write("In this section, consider potential AI related harms and consequences that may arise from the system and describe your ideas for mitigations")

st.markdown(":closed_book: **Definition:** The <ins>Allocation of resources and opportunities</ins> fairness goal applies to AI systems that generate outputs that directly affect the allocation of resources or opportunities relating to finance, education, employment, healthcare, housing, insurance, or social welfare.", unsafe_allow_html=True)

st.write("#### Potential Harms")

helper.potential_harms_hint(st, rai_guide.f2_guide)

all_stakeholders = helper.get_stakeholders(st)

f_enum = helper.Task.F3.value

if 'all_system_info' in st.session_state and st.session_state['all_system_info'] != "":
    sys_info = st.session_state['all_system_info']
else:
    sys_info = f"I am building the following AI application. {st.session_state.get('system_description', '__')} {st.session_state.get('system_purpose', '__')} An user story is {st.session_state.get(f'us1_des', '').strip()}"

if all_stakeholders != [] and f'{f_enum}_task_status' not in st.session_state:
    helper.send_req(st, sys_info, f_enum, all_stakeholders)
    print("sending request for f2")

f2_brainstorm = st.button("Help me brainstorm scenarios concerning Allocation of resources and opportunities", use_container_width=True, type='primary')

if f'f2_clicked' in st.session_state and f'{f_enum}_result' in st.session_state:
    with st.container(border=True):
        write_scenarios(f_enum)
        display_buttons()

if f2_brainstorm:
    if all_stakeholders != []:
        st.session_state[f'f2_clicked'] = True
        helper.wait_response(st, f_enum)
    else:
        st.write("Please fill in stakeholders first")


st.session_state[f'goal_f2_2'] =  st.text_area(f":lower_left_ballpoint_pen: **Instruction: Describe any potential harms**. For each identified stakeholder (:orange[{', '.join(all_stakeholders)}]) that are relevant, consider the potential negative impacts and fairness issues that could arise from the system's deployment and use.", value=st.session_state.get(f"goal_f2_2", ""))

st.write("#### Mitigations")

st.write("After identifying potential harms, propose practical strategies to mitigate these issues.")

st.markdown(":grey_question: **Hint:** Consider both technical solutions and policy measures. Focus on actions that can be taken at various stages of your system's lifecycle to promote fairness.", help="Examples of mitigation strategies for 'Allocation of resources and opportunities' realted harms include evaluating the data sets and the system then modifying the system to minimize differences in the allocation of resources and opportunities between identified demographic groups.\n\n e.g. A hiring system that scans resumes and recommends candidates for hiring trained on historical data tends to be biased toward male candidates. The system can be evaluated and modified to reduce unfair allocation of opportunities.")

st.session_state[f'goal_f2_3'] =  st.text_area(":lower_left_ballpoint_pen: **Instruction: Describe your ideas for mitigations**. List the actions you might take to mitigate the potential harms and fairness issues you have identified.", value=st.session_state.get(f"goal_f2_3", ""))

st.write(":red[END OF STUDY] - Thank for for participating!")

def convert_json():
    data = {
        "stakeholders": all_stakeholders,
    }
    if f'{f_enum}_result' in st.session_state:
        data["generated_scenarios"] = st.session_state[f'{f_enum}_result']

    return json.dumps(data, indent=4)

st.download_button(
    label="Export results to JSON file",
    data=convert_json(),
    file_name='results.json',
    mime='application/json',
)

menu(st)
