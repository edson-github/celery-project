from fastapi import FastAPI
from tasks import soma, tarefa_lenta

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/somar/")
def somar(a: int, b: int):
    tarefa = soma.delay(a, b)
    return {"task_id": tarefa.id}


@app.get("/status/{task_id}")
def status(task_id: str):
    from tasks import celery
    task = celery.AsyncResult(task_id)
    return {
        "task_id": task.id,
        "status": task.status,
        "result": task.result
    }


@app.get("/tarefa-lenta/")
def executar_tarefa_lenta():
    tarefa = tarefa_lenta.delay()
    return {"task_id": tarefa.id}
