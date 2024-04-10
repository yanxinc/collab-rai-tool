import requests
from enum import Enum
import os

class Task(Enum):
    DIRECT_SH = 1
    INDIRECT_SH = 2
    F1 = 3
    F2 = 4
    F3 = 5
    MORE_STAKEHOLDERS = 6

backend_url = os.getenv('BACKEND_URL', "http://0.0.0.0:8502")


def more_stakeholers(st,task_id,task_type):
    response = requests.get(f"{backend_url}/get-more-scenarios/{task_id}")
    if response.status_code == 200:
        result = response.json()
        if result.get('result') != "Task not completed or does not exist":
            st.session_state[f'{task_type}_task_status_unpicked'] = 'Completed'
            return result['result']
    return None

def send_req(st, sys_info, task_type, stakeholders=None):
    response = requests.post(f"{backend_url}/pipeline-req",json={"sys_info": sys_info, "task": task_type, "stakeholders": stakeholders})
    if response.status_code == 200:
        st.session_state[f'{task_type}_task_id'] = response.json()['task_id']
        st.session_state[f'{task_type}_task_status'] = 'Running'
    else:
        st.error("Failed to start background task")

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