from sqlalchemy import Column, String, Text, Integer
from api.database.curd import Base
from pyprojroot import here
import sys
sys.path.append(str(here()))

class QueryAnswer(Base):
    __tablename__ = 'qa'
    id = Column(Integer, primary_key=True)
    task_id = Column(String(255), unique=True)
    query = Column(Text)
    result = Column(Text)