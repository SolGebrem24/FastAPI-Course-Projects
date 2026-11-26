from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=300)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1920, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5,
                'published_date': 2029
            }
        }
    }


BOOKS = [
Book(1, 'A Brief History of Time', 'Stephen Hawking', 'Explores the universe, including black holes, space, time, and the origins of the cosmos.', 5, 1988),
Book(2, 'Introduction to Linear Algebra', 'Gilbert Strang', 'Introduces linear algebra concepts, including vectors, matrices, linear transformations, and eigenvalues.', 5, 1976),
Book(3, 'Clean Code', 'Robert C. Martin', 'Presents practical principles and techniques for writing readable, maintainable, and efficient software.', 5, 2008),
Book(4, 'The Great Gatsby', 'F. Scott Fitzgerald', 'A novel exploring wealth, love, ambition, and the American Dream during the 1920s.', 4, 1925),
Book(5, 'Principles of Economics', 'N. Gregory Mankiw', 'Explains fundamental economic principles, including supply and demand, markets, inflation, and economic growth.', 5, 1997),
Book(6, 'Artificial Intelligence: A Modern Approach', 'Stuart Russell and Peter Norvig', 'Provides a comprehensive introduction to artificial intelligence, including machine learning, search algorithms, knowledge representation, and intelligent agents.', 5, 1995)
]


@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


@app.get("/books/", status_code=status.HTTP_200_OK)
def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/publish/", status_code=status.HTTP_200_OK)
def read_books_by_publish_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
