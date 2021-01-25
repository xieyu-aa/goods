from ..celery import app
import random
from django_redis import get_redis_connection
import time

@app.task(bind=True)
def send_sms(self, mobile):
    time.sleep(10)


    return sms_code