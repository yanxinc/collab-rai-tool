import requests
from enum import Enum
import os, time

class Task(Enum):
    DIRECT_SH = 1
    INDIRECT_SH = 2
    F1 = 3
    F2 = 4
    F3 = 5
    MORE_STAKEHOLDERS = 6

backend_url = os.getenv('BACKEND_URL', "http://0.0.0.0:8502")

def format_scenario_result(scenario, i):
    return f"""
**Scenario {i+1}: {scenario[0]}**\n
{scenario[1]}\n\n
"""

def more_scenarios(st,task_id,task_type):
    response = requests.get(f"{backend_url}/get-more-scenarios/{task_id}")
    if response.status_code == 200:
        result = response.json()
        if result.get('result') != "Task not completed or does not exist":
            st.session_state[f'{task_type}_task_status_unpicked'] = 'Completed'
            return result['result']
    return None

def send_req(st, sys_info, task_type, stakeholders=None, feedback=None):
    response = requests.post(f"{backend_url}/pipeline-req",json={"sys_info": sys_info, "task": task_type, "stakeholders": stakeholders, "feedback": feedback})
    if response.status_code == 200:
        st.session_state[f'{task_type}_task_id'] = response.json()['task_id']
        st.session_state[f'{task_type}_task_status'] = 'Running'
    else:
        st.error("Failed to start background task")

def wait_response(st, f_enum):
    if f'{f_enum}_task_status' in st.session_state and st.session_state[f'{f_enum}_task_status'] == 'Running':
        with st.spinner('Generating Scenarios...'):
            while True:
                result = poll_task_status(st, st.session_state[f'{f_enum}_task_id'], f_enum)
                if result:
                    st.session_state[f"{f_enum}_result"] = result
                    st.rerun()
                else:
                    time.sleep(10)

def start_study(i):
    requests.get(f"{backend_url}/start-study/{i}")

# Polling mechanism
def poll_task_status(st,task_id, task_type):
    response = requests.get(f'{backend_url}/get-result/{task_id}')
    if response.status_code == 200:
        result = response.json()
        if result.get('result') != "Task not completed or does not exist":
            st.session_state[f'{task_type}_task_status'] = 'Completed'
            return result['result']
    return None

def get_stakeholders(st):
    if f'direct_stakeholders' not in st.session_state:
        direct_stakeholders = []
    else:
        df = st.session_state[f'direct_stakeholders']
        direct_stakeholders = df[df['Direct Stakeholders'] != '']['Direct Stakeholders'].tolist()

    if f'indirect_stakeholders' not in st.session_state:
        indirect_stakeholders = []
    else:
        df = st.session_state[f'indirect_stakeholders']
        indirect_stakeholders = df[df['Indirect Stakeholders'] != '']['Indirect Stakeholders'].tolist()

    return list(set(direct_stakeholders + indirect_stakeholders))

def potential_harms_hint(st, guide):
    hint = f"""
:grey_question: **Hint:** {guide} Consider <span class="tooltip">marginalized groups<span class="tooltiptext">**Marginalized groups** are demographic groups who may have an atypical or even unfair experience with the system if their needs and context are not considered. May include minorities, stigmatized groups, or other particularly vulnerable groups. Additionally, marginalized groups can also include children, the elderly, indigenous peoples, and religious minorities. Groups to include for consideration will depend in part on the geographic areas and intended uses of your system.</span></span> and think about different <span class="tooltip">demographic group<span class="tooltiptext">**Demographic groups** can refer to any population group that shares one or more particular demographic characteristics. Depending on the AI system and context of deployment, the list of identified demographic groups will change.</span></span> of stakeholders.
"""

    css = """
<style>
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black; /* Optional: underline the hoverable text */
}

.tooltip .tooltiptext {
    visibility: hidden;
    width: 50vw; /* 50% of the viewport width */
    background-color: black;
    color: #fff;
    text-align: center;
    border-radius: 6px;
    padding: 5px;
    
    /* Position the tooltip */
    position: absolute;
    z-index: 1;
    bottom: 100%;
    left: 50%;
    margin-left: -25vw; /* This ensures the tooltip is centered relative to the hoverable text */
    overflow: hidden; /* Prevents the text from spilling out of the tooltip box */
}

.tooltip:hover .tooltiptext {
    visibility: visible;
}
</style>
"""

    st.markdown(css + hint, unsafe_allow_html=True)

def write_scenarios(st, f_enum, st_feedback):
    scenario_heading_list = st.session_state[f'{f_enum}_result']
    for i in range(len(scenario_heading_list)):
        c1, c2 = st.columns([0.7,0.3])
        with c1:
            st.write(format_scenario_result(scenario_heading_list[i], i))
            
        with c2:
            _, c4 = st.columns([0.9, 0.1])
            with c4:
                st.markdown("", help="If you did not like a scenario, consider providing feedback to help improve the quality for the regenerated sceanrios.\n - Was the scenario relevant? If not, what information can be added to make it relevant?\n - Were there anything that was misunderstood?\n - Would you like to clarify some information?")
            st_feedback(feedback_type="thumbs", key=f's{i}_thumbs', optional_text_label='Optional explanation')

    st.write(":red[Note: The generated scenarios are only examples of potential harms and fairness issues that could arise from the system's deployment and use. They are potential starting points for considering the fairness implications of the system. We cannot guarantee the accuracy and completeness of the information provided. Please think beyond the generated sceanrios and do not limit your brainstorming of harms to these scenarios.]")

def display_buttons(st, f_enum, sys_info, all_stakeholders):
    c3, c4 = st.columns([0.5,0.5])
    with c3:
        if f'{f_enum}_result_unpicked' not in st.session_state:
            more_scenarios_btn = st.button("Show more scenarios", key=f"{f_enum}_more_scenarios",use_container_width=True)
            if more_scenarios_btn:
                result = more_scenarios(st, st.session_state[f'{f_enum}_task_id'], f_enum)
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

                send_req(st, sys_info, f_enum, all_stakeholders, feedback)
                print(f"sending regenerate request for f{f_enum-2} with feedback: {feedback}")
                wait_response(st, f_enum)
                st.rerun()