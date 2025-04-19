from datetime import timedelta, datetime

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from pymongo.errors import InvalidOperation

from transaction.models import transaction_collection, transaction_summary_collection


# this command will summarize all transactions of a merchant in a single day
# TODO: it would be better to summarize all transaction in a day.
# TODO: it would be better to summarize all transaction of a merchant in a week.
# TODO: it would be better to summarize all transaction in a week.
# TODO: it would be better to summarize all transaction of a merchant in a month.
# TODO: it would be better to summarize all transaction in a month.
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "start",
        )

    def handle(self, *args, **kwargs):
        start_of_day = kwargs['start']
        results = self.get_today_transactions(start_of_day)
        try:
            res = transaction_summary_collection.insert_many(results)
        except InvalidOperation as err:
            print(err)
        else:
            print(f'{len(res.inserted_ids)} record inserted in summary collection for day {start_of_day}')

    def get_today_transactions(self, start_of_day):
        collection = transaction_collection
        start_of_day = datetime.strptime(start_of_day, "%Y-%m-%d").replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)

        pipeline = [
            {
                # Match documents for the given day and optional merchant_id
                "$match": {
                    "created_at": {
                        "$gte": start_of_day,
                        "$lt": end_of_day
                    }
                }
            },
            {
                # Group by merchant_id to calculate count and sum of amount
                "$group": {
                    "_id": "$merchant_id",
                    "count": {"$sum": 1},  # Count of records
                    "total_amount": {"$sum": "$amount"}  # Sum of amount
                }
            },
            {
                # Project to format the output
                "$project": {
                    "_id": 0,
                    "created_at": start_of_day,
                    "merchant_id": "$_id",
                    "count": 1,
                    "total_amount": 1
                }
            }
        ]
        results = collection.aggregate(pipeline)
        return results
