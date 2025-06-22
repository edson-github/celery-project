from celery import Celery

celery = Celery('tasks')
celery.config_from_object('celeryconfig')


@celery.task
def soma(x, y):
    return x + y


@celery.task
def tarefa_lenta():
    import time
    time.sleep(10)
    return 'Tarefa concluída após 10 segundos'
