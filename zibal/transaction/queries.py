from typing import Optional


class Mode:
    def get_group_id(self):
        raise NotImplementedError

    def get_project_key(self):
        raise NotImplementedError


class DailyData(Mode):
    def get_group_id(self):
        group_id = {
            "year": {"$year": "$created_at"},
            "month": {"$month": "$created_at"},
            "day": {"$dayOfMonth": "$created_at"}
        }
        return group_id

    def get_project_key(self):
        date_format = "%Y-%m-%d"
        key = {
            "$dateToString": {
                "format": date_format,
                "date": {
                    "$dateFromParts": {
                        "year": "$_id.year",
                        "month": "$_id.month",
                        "day": "$_id.day"
                    }
                }
            }
        }
        return key


class WeeklyData(Mode):
    def get_group_id(self):
        group_id = {
            "year": {"$year": "$created_at"},
            "week": {"$week": "$created_at"}
        }
        return group_id

    def get_project_key(self):
        key = {
            "$concat": [
                {"$toString": "$_id.year"},
                "-",
                {"$cond": [
                    {"$lt": ["$_id.week", 10]},
                    {"$concat": ["0", {"$toString": "$_id.week"}]},
                    {"$toString": "$_id.week"}
                ]}
            ]
        }
        return key


class MonthlyData(Mode):
    def get_group_id(self):
        group_id = {
            "year": {"$year": "$created_at"},
            "month": {"$month": "$created_at"}
        }
        return group_id

    def get_project_key(self):
        date_format = "%Y-%m"
        key = {
            "$dateToString": {
                "format": date_format,
                "date": {
                    "$dateFromParts": {
                        "year": "$_id.year",
                        "month": "$_id.month",
                        "day": 1
                    }
                }
            }
        }
        return key


def get_mode(mode_name: str) -> 'Mode':
    if mode_name == 'daily':
        return DailyData()
    elif mode_name == 'weekly':
        return WeeklyData()
    elif mode_name == 'monthly':
        return MonthlyData()
    else:
        raise ValueError('Invalid mode. Options are `daily`, `weekly` and `monthly`.')


class AggregateData:
    def __init__(self):
        self.merchant_id = None
        self.mode = None
        self.query_type = None
        self.pipeline = []

    def set_merchant_id(self, merchant_id: Optional[int]):
        self.merchant_id = merchant_id

    def set_mode(self, mode: str):
        self.mode = get_mode(mode_name=mode)

    def set_type(self, query_type: str):
        if query_type == 'count':
            self.query_type = 1
        elif query_type == 'amount':
            self.query_type = "$amount"
        else:
            raise ValueError('Invalid type. options are `count` and `amount`.')

    def get_pipeline(self):
        # reset pipeline
        self.pipeline = []

        # stage0: merchant_id
        if self.merchant_id is not None:
            self.pipeline.append({"$match": {"merchant_id": self.merchant_id}})

        # stage1: group
        self.pipeline.append(
            {
                # Group by the date components
                "$group": {
                    "_id": self.mode.get_group_id(),
                    "value": {
                        "$sum": self.query_type
                    }
                }
            }
        )

        # stage2: project
        self.pipeline.append(
            {
                # Project to format the key and value
                "$project": {
                    "_id": 0,
                    "key": self.mode.get_project_key(),
                    "value": 1
                }
            }
        )

        # stage3: project
        self.pipeline.append(
            {
                # Sort by key (date)
                "$sort": {"key": 1}
            }
        )
        return self.pipeline
