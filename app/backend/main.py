from fastapi import FastAPI, BackgroundTasks
import uvicorn
import time
import uuid
import pipeline
from pydantic import BaseModel
from typing import List,Optional
import os, sys, re
app_dir = os.path.dirname(__file__)
helpers_dir = os.path.join(app_dir, 'helpers')
sys.path.append(helpers_dir)
from helper import Task
from fastapi.responses import HTMLResponse

class Data(BaseModel):
    sys_info: str
    task: int
    stakeholders: Optional[List[str]] = None

app = FastAPI()
results = {}

def process_unpicked_scenarios(unpicked, stakeholders):
    final_scenarios = pipeline.remove_correctives(unpicked)

    scenario_heading_list = [
        (pipeline.generate_heading(scenario, stakeholders), re.sub(r'^\d+\.\s*', '', scenario.strip()).strip()) for scenario in final_scenarios
    ]
    return scenario_heading_list

def background_task(data: Data, task_id: str, task: Task):
    sys_info = data.sys_info
    match task:
        case Task.DIRECT_SH:
            print("Start Generating Direct Stakeholders...")
            print("System Info: ", sys_info)
            results[task_id] = pipeline.get_direct_stakeholders(sys_info)
            print("Direct Stakeholders Generated")
        case Task.INDIRECT_SH:
            print("Start Generating Indirect Stakeholders...")
            results[task_id] = pipeline.get_indirect_stakeholders(sys_info)
            print("Indirect Stakeholders Generated")
        case Task.F1:
            print("Start Generating F1 Scenarios...")
            print(data.stakeholders)

            picked, unpicked = pipeline.generate_scenarios(sys_info, 'f1', data.stakeholders)
            results[task_id] = picked
            print("F1 Scenarios Generated")

            results[task_id + "_unpicked"] = process_unpicked_scenarios(unpicked,data.stakeholders)
        case Task.F2:
            print("Start Generating F2 Scenarios...")
            print(data.stakeholders)

            picked, unpicked = pipeline.generate_scenarios(sys_info, 'f2', data.stakeholders)
            results[task_id] = picked
            print("F2 Scenarios Generated")

            results[task_id + "_unpicked"] = process_unpicked_scenarios(unpicked,data.stakeholders)
        case Task.F3:
            print("Start Generating F3 Scenarios...")
            print(data.stakeholders)

            picked, unpicked = pipeline.generate_scenarios(sys_info, 'f3', data.stakeholders)
            results[task_id] = picked
            print("F3 Scenarios Generated")

            results[task_id + "_unpicked"] = process_unpicked_scenarios(unpicked,data.stakeholders)

@app.post("/pipeline-req/")
async def run_task(data: Data, background_tasks: BackgroundTasks):
    print(f"Received Request: {Task(data.task)}")

    task_id = str(uuid.uuid4())

    background_tasks.add_task(background_task, data=data, task_id=task_id, task=Task(data.task))
    return {"task_id": task_id}

@app.get("/get-result/{task_id}")
async def get_result(task_id: str):
    # Retrieve the result using the task ID, or return a default message
    result = results.get(task_id, "Task not completed or does not exist")
    return {"task_id": task_id, "result": result}

@app.get("/get-more-scenarios/{task_id}")
async def get_more_scenarios(task_id: str):
    unpicked = results.get(task_id + "_unpicked", "Task not completed or does not exist")

    return {"task_id": task_id, "result": unpicked}

@app.get("/logs")
def logs():
    html_content = "<html><body><pre>"
    html_content+= "<h1>Logs</h1>"
    html_content+= "<h4>Note: The logs are displayed in reverse line order</h4>"
    with open('results.log', 'r') as file:
        lines = file.readlines()
        for line in reversed(lines):
            html_content += f"{line.strip()}<br>"
    html_content += "</pre></body></html>"
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8502)
