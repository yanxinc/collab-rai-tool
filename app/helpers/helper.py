import requests
from enum import Enum
import os

class Task(Enum):
    DIRECT_SH = 1
    INDIRECT_SH = 2
    F1 = 3
    F2 = 4
    F3 = 5

backend_url = os.getenv('BACKEND_URL', "http://0.0.0.0:8502")


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
        direct_stakeholders = df[df['Stakeholders'] != '']['Stakeholders'].tolist()

    if f'indirect_stakeholders' not in st.session_state:
        indirect_stakeholders = []
    else:
        df = st.session_state[f'indirect_stakeholders']
        indirect_stakeholders = df[df['Stakeholders'] != '']['Stakeholders'].tolist()

    return direct_stakeholders + indirect_stakeholders
