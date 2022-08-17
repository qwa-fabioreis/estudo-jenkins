from celery import Celery
import os

redis_url = os.environ.get("REDIS_URL", 'redis://localhost:6379')

celery = Celery(__name__, backend="%s/0" % redis_url, broker="%s/1" % redis_url,
                include=('app.src.service.image_process',))


def create_app(app):

    celery.conf.update(app.config)