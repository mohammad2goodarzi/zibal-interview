import requests
import environ


env = environ.Env()


class NotificationController:
    def __init__(self):
        pass

    def notify(self, message, user):
        raise NotImplementedError


class TelegramController(NotificationController):
    def notify(self, message, user):
        api_token = env('telegram_api_token', default='foo')
        api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'
        try:
            response = requests.post(api_url, json={'chat_id': user, 'text': message})
            response.raise_for_status()
        except Exception as e:
            # just capturing logs
            print(e)
            raise


class EmailController(NotificationController):
    pass


class SMSController(NotificationController):
    pass


def get_notification_controller(medium_type: str):
    if medium_type == 'sms':
        return SMSController
    elif medium_type == 'email':
        return EmailController
    elif medium_type == 'telegram':
        return TelegramController
    else:
        raise ValueError('invalid medium. options are `sms`, `email` and `telegram`')
