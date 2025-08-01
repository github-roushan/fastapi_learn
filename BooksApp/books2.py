from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_year: int

class BookRequest(BaseModel):
     id: Optional[int] = Field(description="Id is not needed on create", default=None)
     title: str = Field(min_length=3)
     author: str = Field(min_length=1)
     description: str = Field(min_length=1, max_length=100)
     rating: int = Field(gt=-1, lt=6)
     published_year: int = Field(gt=0)

     class Config:
          json_schema_extra = {
               "example": {
                    "title": "FastAPI: CookBook",
                    "author": "Roushan Singh",
                    "description": "Get Up and Going with FastAPI",
                    "rating": 5,
                    "published_date": 1997
               }
          }

BOOKS: List["Book"] = [
    Book(1, "Dune", "Frank Herbert",
         "A richly detailed epic about politics, religion, and ecology on the desert planet Arrakis—considered one of the greatest sci‑fi novels of all time.",
         5, 1965),
    Book(2, "Sapiens: A Brief History of Humankind", "Yuval Noah Harari",
         "A sweeping, accessible exploration of human evolution, societies, and how our species shaped the world.",
         4, 2011),
    Book(3, "To Kill a Mockingbird", "Harper Lee",
         "A powerful classic of racial injustice and moral growth in the American South, seen through a child's eyes.",
         5, 1960),
    Book(4, "1984", "George Orwell",
         "A chilling dystopia about total surveillance and oppressive power—still eerily relevant today.",
         5, 1949),
    Book(5, "The Name of the Wind", "Patrick Rothfuss",
         "The lyrical and immersive first‑person tale of Kvothe’s childhood, magic-training, and quest for revenge.",
         4, 2007),
    Book(6, "The Midnight Library", "Matt Haig",
         "A touching, philosophical novel exploring regret and the many paths a life can take via a magical library.",
         4, 2020),
    Book(7, "Educated", "Tara Westover",
         "A gripping memoir of a woman who escaped a survivalist upbringing through education and self-discovery.",
         5, 2018),
    Book(8, "Project Hail Mary", "Andy Weir",
         "A thrilling, science‑heavy space adventure where a lone astronaut must save Earth—with humor, technical ingenuity, and an alien companion Rocky.",
         5, 2021),
    Book(9, "The Silent Patient", "Alex Michaelides",
         "A tense psychological thriller about a woman who stops speaking after shooting her husband—and the psychotherapist obsessed with uncovering why.",
         4, 2019),
    Book(10, "The Alchemist", "Paulo Coelho",
         "A modern allegory about following your dreams filled with mystical encounters and insights on destiny.",
         4, 1988),
    Book(11, "Children of Dune", "Frank Herbert",
         "The continued saga of Paul Atreides’ legacy as Arrakis descends into political and religious upheaval.",
         4, 1976)
]

NEXT_ID = len(BOOKS)

app = FastAPI()
@app.get("/books", status_code=status.HTTP_200_OK)
async def get_all_books():
     return BOOKS

@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = [book for book in BOOKS if book.rating == book_rating]
    return books_to_return

@app.get("/books/year/", status_code=status.HTTP_200_OK)
async def get_books_by_published_year(published_year: int = Query(gt=1929)):
    books_to_return = [book for book in BOOKS if book.published_year == published_year]
    return books_to_return

@app.post("/books/create_book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    add_id_to_book(new_book)
    BOOKS.append(new_book)
    return {"message": "Book created successfully"}

def add_id_to_book(book: Book):
     global NEXT_ID
     NEXT_ID += 1
     book.id = NEXT_ID

@app.put("/books/update_book", status_code=status.HTTP_200_OK)
async def update_book(book_request: BookRequest):
     updated_book = Book(**book_request.model_dump())
     for ind, book in enumerate(BOOKS):
          if book.id == updated_book.id:
               BOOKS[ind] = updated_book
               return {"message": "Book updated successfully"}
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: int = Path(gt=0)):
     for i in range(len(BOOKS)):
          if BOOKS[i].id == book_id:
               BOOKS.pop(i)
               return {"message": "Book deleted successfully"}
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")