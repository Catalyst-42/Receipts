from enum import StrEnum, auto


class TransactionType(StrEnum):
    INCOME = auto()
    OUTCOME = auto()
