import random
from bson import ObjectId
from django.utils import timezone

from notification.controllers import get_notification_controller
from notification.models import notification_collection
from zibal.celery import app


@app.task(autoretry_for=(Exception,), max_retries=30)
def send_notification(inserted_id):
    obj = notification_collection.find_one({'_id': ObjectId(inserted_id)})
    controller_class = get_notification_controller(obj['medium'])
    result = controller_class().notify(obj['message'], obj['user'])
    notification_collection.update_one(
        {'_id': ObjectId(inserted_id)},
        {
            '$set': {
                'notified': True,
                'sent_at': timezone.now(),
            }
        }
    )
    return result
