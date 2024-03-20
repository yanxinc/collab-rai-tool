from fastapi import FastAPI, BackgroundTasks
import uvicorn
import time
import uuid
import pipeline
from pydantic import BaseModel
from helper import Task

class Data(BaseModel):
    sys_info: str
    task: int

app = FastAPI()
results = {}

def background_task(sys_info: str, task_id: str, task: Task):
    match task:
        case Task.DIRECT_SH:
            print("Start Generating Direct Stakeholders...")
            print("System Info: ", sys_info)
            results[task_id] = pipeline.get_direct_stakeholders(sys_info)

            # time.sleep(10)
            # results[task_id] = "Direct Stakeholders Generated"

            print("Direct Stakeholders Generated")
        case Task.INDIRECT_SH:
            print("Start Generating Indirect Stakeholders...")
            results[task_id] = pipeline.get_indirect_stakeholders(sys_info)

            # time.sleep(10)
            # results[task_id] = "Indirect Stakeholders Generated"

            print("Indirect Stakeholders Generated")


@app.post("/pipeline-req/")
async def run_task(data: Data, background_tasks: BackgroundTasks):
    print(f"Received Request: {data.task}")

    task_id = str(uuid.uuid4())

    background_tasks.add_task(background_task, sys_info=data.sys_info, task_id=task_id, task=Task(data.task))
    return {"task_id": task_id}

@app.get("/get-result/{task_id}")
async def get_result(task_id: str):
    # Retrieve the result using the task ID, or return a default message
    result = results.get(task_id, "Task not completed or does not exist")
    return {"task_id": task_id, "result": result}

if __name__ == "__main__":
    uvicorn.run("main:app")
