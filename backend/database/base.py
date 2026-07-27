from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


import database.models  # noqa