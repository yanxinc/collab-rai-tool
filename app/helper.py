import requests
from enum import Enum

class Task(Enum):
    DIRECT_SH = 1
    INDIRECT_SH = 2


def send_req(st, sys_info, task_type):
    ENDPOINT = f"http://localhost:8000/pipeline-req"
    response = requests.post(ENDPOINT,json={"sys_info": sys_info, "task": task_type})
    if response.status_code == 200:
        st.session_state[f'{task_type}_task_id'] = response.json()['task_id']
        st.session_state[f'{task_type}_task_status'] = 'Running'
    else:
        st.error("Failed to start background task")

# Polling mechanism
def poll_task_status(st,task_id, task_type):
    response = requests.get(f'http://localhost:8000/get-result/{task_id}')
    if response.status_code == 200:
        result = response.json()
        if result.get('result') != "Task not completed or does not exist":
            st.session_state[f'{task_type}_task_status'] = 'Completed'
            return result['result']
    return None