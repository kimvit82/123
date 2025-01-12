from sqlalchemy import *
from sqlalchemy.orm import *

engine = create_engine('sqlite:///4urok.db')
Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship("Book", back_populates="authors")

class Book(Base):
    __tablename__="books"
    id = Column(Integer, primary_key=True)
    title = Column(String,nullable=False)

    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")

Base.metadata.create_all(engine)
Session= sessionmaker(bind=engine)
session = Session()

def add_author(name):
    new_author = Author(name=name)
    session.add(new_author)

confirm = input("Вы хотите создать нового автора? Нажмитe = 1, Если нет = 2:")

while confirm == "1":
    name = input("Введите имя автора:")
    add_author(name)
    session.commit()
    print("Автор с именем", name, "успешо сохранился в базе данных")
    confirm = input("Вы хотите создать нового автора?: Нажмите = 1. Если нет = 2:")

Base.metadata.create_all(engine)

def add_book(title, author_id):
    new_book = Book(title=title, author=author_id)
    session.add(new_book)
    session.commit()
