from datetime import datetime
import random
import time

from django.core.management import BaseCommand

from transaction.models import transaction_collection


def get_random_date(since=2023, until=2025, number_of_days=28, number_of_months=12, **kwargs):
    year = random.randint(since, until)
    month = random.randint(1, number_of_months)
    day = random.randint(1, number_of_days)
    return datetime(year, month, day)


def get_random_amount(lower_bound=100000, upper_bound=1000000000, unit=10000, **kwargs):
    amount = random.randint(lower_bound, upper_bound)
    amount //= unit
    amount *= unit
    return amount


def get_random_merchant_id(number_of_merchants=10000, **kwargs):
    merchant_id = random.randint(1, number_of_merchants)
    return merchant_id


def get_record_as_dict(**kwargs):
    date = get_random_date(**kwargs)
    amount = get_random_amount(**kwargs)
    merchant_id = get_random_merchant_id(**kwargs)
    return {'created_at': date, 'merchant_id': merchant_id, 'amount': amount}


# this can be used like this:
# python manage.py initial_data 3000000 1000 --number_of_months 12 --since 2024 --until 2024 --number_of_days 10 --number_of_merchants 500
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "data_size",
            type=int,
        )
        parser.add_argument(
            "batch_size",
            type=int,
        )
        parser.add_argument(
            "--since",
            default=2023,
            type=int,
        )
        parser.add_argument(
            "--until",
            default=2023,
            type=int,
        )
        parser.add_argument(
            "--number_of_months",
            default=12,
            type=int,
        )
        parser.add_argument(
            "--number_of_days",
            default=28,
            type=int,
        )
        parser.add_argument(
            "--number_of_merchants",
            default=10000,
            type=int,
        )

    def handle(self, *args, **kwargs):
        # this command generate `data_size` random data
        # since `--since` year until `--until` year.
        # from the first month, until the `--number_of_months`'th month
        # from the first day, until the `--number_of_days`'th day
        # there are `--number_of_merchants` unique merchant id in these data
        data_size = kwargs['data_size']
        batch_size = kwargs['batch_size']
        t1 = time.time()
        data = []
        for i in range(data_size):
            data.append(get_record_as_dict(**kwargs))
            if (i + 1) % batch_size == 0:
                transaction_collection.insert_many(data)
                data = []
        if len(data) != 0:
            transaction_collection.insert_many(data)
        t2 = time.time()
        print(f'{data_size} data inserted in {round(t2 - t1, 3)} seconds')
