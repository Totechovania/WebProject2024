import datetime
import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Codes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'codes'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    update_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
