from celery import Celery
from flask import Flask
from app.extensions import db

celery = Celery('app')
celery.config_from_object('app.celeryconfig')

# Optionnel : intégration Flask context

def make_celery(app: Flask):
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery 
