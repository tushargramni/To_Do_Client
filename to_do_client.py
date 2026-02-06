from fastapi import FastAPI
from pydantic import BaseModel
from starlette import status


class Task(BaseModel):
    title:str
    description:str
    status:str
app = FastAPI()
task_dict = {}
@app.get("/")
def root():
    return {"Add some Task"}

@app.get("/tasks", status_code=status.HTTP_200_OK)
def get_all_tasks():
    return {task_id: task.model_dump() for task_id, task in task_dict.items()}

@app.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def get_specific_task(task_id: int):
    task = task_dict.get(task_id)
    if task:
        return task.model_dump()
    return {"No Such Task"}

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task_id: int, task: Task):
    if task_id not in task_dict:
        task_dict[task_id] = task
        return {"message": "Task Created Successfully", "task": task.model_dump()}
    else:
        return {"error": "Task already exists"}

@app.patch("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def update_task_status(task_id: int, is_complete: str):
    if task_id in task_dict:
        task_dict[task_id].status = is_complete
        return {"message": "Task updated", "task": task_dict[task_id].model_dump()}
    else:
        return {"error": "No Such Task"}


@app.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int):
    if task_id in task_dict:
        del task_dict[task_id]
        return {"message": "Task deleted successfully"}
    else:
        return {"error": "No Such Task"}

# if __name__ == "__main__":
#     print(get_all_tasks())
#
#     print(get_specific_task(1))
#
#     print(create_task(3,Task(title="Task-3", description="task -3 added, new self create itself from nothing",status="is_pending")))
#     print(create_task(1, Task(title="Task-1", description="task -2 added, Enjoy every moment of life without worry and amazingly.",status="is_pending")))
#
#     print(get_specific_task(1))
#     print(get_all_tasks())
#
#     print(update_task_status(1,"completed"))
#
#     print(delete_task(1))
#     print(get_all_tasks())
