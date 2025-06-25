"""
Extensions Flask pour la toolbox
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from celery import Celery
import redis

# Base de données
db = SQLAlchemy()

# Migrations
migrate = Migrate()

# JWT
jwt = JWTManager()

# Redis
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

# Celery
celery = Celery(
    'toolbox',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=[
        'modules.discovery.tasks',
        'modules.vulnerability.tasks',
        'modules.exploitation.tasks',
        'modules.forensics.tasks',
        'modules.reporting.tasks'
    ]
)

# Configuration Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
) 