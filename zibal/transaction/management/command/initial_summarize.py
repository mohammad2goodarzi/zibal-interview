from datetime import datetime, timedelta

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "start",
        )
        parser.add_argument(
            "end",
            default=None,
        )

    def handle(self, *args, **kwargs):
        start_of_day = kwargs['start']
        end_of_day = kwargs['end']
        start_date = datetime.strptime(start_of_day, "%Y-%m-%d")
        end_date = datetime.strptime(end_of_day, "%Y-%m-%d")
        current_date = start_date
        while current_date < end_date:
            current_day_str = current_date.strftime("%Y-%m-%d")
            call_command('summarize', current_day_str)
            current_date += timedelta(days=1)