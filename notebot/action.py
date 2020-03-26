from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///notes.sqlite', echo=True)

Base = declarative_base()
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    text = Column(String)
    author = Column(String)

    def __init__(self, name, text, author):
        self.name = name
        self.text = text
        self.author = author
    def __repr__(self):
        return f'Note #{self.id}: {self.name} by {self.author}'

#Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

note = Note('First', 'Text for thid note', 'Mike')
session.add(note)
session.commit()

