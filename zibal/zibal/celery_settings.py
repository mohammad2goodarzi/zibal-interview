from utils import client, url, db

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'  # RabbitMQ broker
CELERY_RESULT_BACKEND = url
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'default',
    'taskmeta_collection': 'celery_taskmeta',
}
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_TRACK_STARTED = True
CELERY_IGNORE_RESULT = False  # Ensure results are stored
MONGO_CLIENT = client
MONGO_DB = db
