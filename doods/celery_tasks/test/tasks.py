from celery_tasks.celery import app

@app.task(bind=True)
def getsum(self,a):
    self.retry()
    return a*100
