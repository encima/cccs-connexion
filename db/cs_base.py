from sqlalchemy import event
from sqlalchemy import Column, DateTime, String, Integer, create_engine, JSON, ForeignKey, Boolean
import uuid
import datetime

def _get_date():
    return datetime.datetime.now()

class CSBase():
    id = Column(String(100), default=uuid.uuid4, primary_key=True)
    created_at = Column(DateTime(), default=_get_date)
    updated_at = Column(DateTime(), onupdate=_get_date)

    def __init__(self):
        self.id = uuid.uuid4()

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])
    


    @staticmethod
    def insert(mapper, connection, target):
        target.created_at = _get_date

    @staticmethod
    def update(mapper, connection, target):
        target.updated_at = _get_date

event.listen(CSBase, 'before_insert', CSBase.insert)
event.listen(CSBase, 'before_update', CSBase.update)