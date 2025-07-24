from enum import StrEnum


class GroupByPeriodEnum(StrEnum):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'
    YEARLY = 'yearly'
    TOTAL = 'total'
