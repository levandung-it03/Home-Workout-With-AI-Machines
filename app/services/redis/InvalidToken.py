import datetime

from aredis_om import HashModel


class InvalidToken(HashModel):
    id: str
    expiryDate: datetime.datetime