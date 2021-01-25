import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doods.settings.dev')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('celery_tasks.config', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(['celery_tasks.test','celery_tasks.sms'])


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task(bind=True)
def tst(self, a):
    return 'you are big%s'% a
# aa = tst.delay('hhhh')
# print(aa.result)
# print(aa.get())