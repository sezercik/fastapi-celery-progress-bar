import time

import uvicorn
from celery import Celery
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, log_level="debug")

celery = Celery(
    "tasks",
    broker="redis://localhost:6379/2",  # Replace with your Redis broker URL
    backend="redis://localhost:6379/3"
)


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/long-process/{data}")
async def ocr(data: int):
    task = ocr_task.delay(data)
    return {"task_id": task.id}


@celery.task(bind=True)
def ocr_task(self, data: int):
    for iteration in range(1,data):
        progress = (iteration) / data * 100
        print(progress)
        time.sleep(3)
        self.update_state(state='PROCESS', meta={'current': iteration, "total": data, 'progress': progress})
    return {"content": "your content like machine learning model result data or samething else"}


@app.get("/result/{task_id}")
async def ocr_result(task_id):
    result = ocr_task.AsyncResult(task_id)
    response = {}

    if result.ready():
        data = result.get(Exception)
        return {"status": "COMPLETED", "data": data}
    elif result.failed():
        raise HTTPException(status_code=422, detail="process failed")
    
    if result.state == "PENDING":
        response = result.info
    elif result.state == "PROCESS":
        response = result.info
    else:
        response = {
            "state": result.state,
            "current": 1,
            "total": 1,
            "status": str(result.info)
        }
    
    return {"status": "PROCESS", "response": response}
