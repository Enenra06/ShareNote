from sqlalchemy import create_engine
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///notes.db', echo=True)
Base = declarative_base()

class Note(Base):

    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    owner = Column(String)
    name = Column(String)
    body = Column(String)

    def __init__(self, owner, name, body):

        self.owner = owner
        self.name = name
        self.body = body

Base.metadata.create_all(engine)


