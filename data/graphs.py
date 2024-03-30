import datetime

import sqlalchemy

from data.db_session import SqlAlchemyBase


class Graph(SqlAlchemyBase):
    __tablename__ = 'graphs'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    private = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    function = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    preview_path = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    update_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    user = sqlalchemy.orm.relationship('User')
