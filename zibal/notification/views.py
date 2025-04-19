from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from notification.models import notification_collection
from notification.tasks import send_notification


class SendNotificationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        now = timezone.now()
        records = []
        # I assumed that it can be multiple medium for a message and a user.
        # so I insert multiple records to the collection
        for medium in request.data['media']:
            records.append(
                {
                    'user': request.data['user'],
                    'message': request.data['message'],
                    'medium': medium,
                    'notified': False,
                    'sent_at': None,
                    'created_at': now,
                }
            )
        objects = notification_collection.insert_many(records)

        # I also assumed that we can and we should try to send notifications right now
        for inserted_id in objects.inserted_ids:
            send_notification.delay(str(inserted_id))
        return Response(f'notification will be sent.')


# TODO: I should implement an API to get reports of notifications.
# but I think it's easy. I have enough data the return reports. I'm just tired.
