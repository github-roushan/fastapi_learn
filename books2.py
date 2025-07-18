from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Book:
     id: int
     title: str
     author: str
     description: str
     rating: int
     
     def __init__(self, id, title, author, description, rating):
          self.id = id
          self.title = title
          self.author = author
          self.description = description
          self.rating = rating
class BookRequest(BaseModel):
     id: int
     title: str
     author: str
     description: str
     rating: int


BOOKS = [
    Book(1,
         "Dune",
         "Frank Herbert",
         "A richly detailed epic about politics, religion, and ecology on the desert planet Arrakis—considered one of the greatest sci‑fi novels of all time.",
         5),
    Book(2,
         "Sapiens: A Brief History of Humankind",
         "Yuval Noah Harari",
         "A sweeping, accessible exploration of human evolution, societies, and how our species shaped the world.",
         4),
    Book(3,
         "To Kill a Mockingbird",
         "Harper Lee",
         "A powerful classic of racial injustice and moral growth in the American South, seen through a child's eyes.",
         5),
    Book(4,
         "1984",
         "George Orwell",
         "A chilling dystopia about total surveillance and oppressive power—still eerily relevant today.",
         5),
    Book(5,
         "The Name of the Wind",
         "Patrick Rothfuss",
         "The lyrical and immersive first‑person tale of Kvothe’s childhood, magic-training, and quest for revenge.",
         4),
    Book(6,
         "The Midnight Library",
         "Matt Haig",
         "A touching, philosophical novel exploring regret and the many paths a life can take via a magical library.",
         4),
    Book(7,
         "Educated",
         "Tara Westover",
         "A gripping memoir of a woman who escaped a survivalist upbringing through education and self-discovery.",
         5),
    Book(8,
         "Project Hail Mary",
         "Andy Weir",
         "A thrilling, science‑heavy space adventure where a lone astronaut must save Earth—with humor, technical ingenuity, and an alien companion Rocky. Critics called it a science‑fiction “masterwork” balanced with engaging narrative and friendship dynamics :contentReference[oaicite:1]{index=1}.",
         5),
    Book(9,
         "The Silent Patient",
         "Alex Michaelides",
         "A tense psychological thriller about a woman who stops speaking after shooting her husband—and the psychotherapist obsessed with uncovering why.",
         4),
    Book(10,
         "The Alchemist",
         "Paulo Coelho",
         "A modern allegory about following your dreams filled with mystical encounters and insights on destiny.",
         4),
    Book(11,
         "Children of Dune",
         "Frank Herbert",
         "The continued saga of Paul Atreides’ legacy as Arrakis descends into political and religious upheaval.",
         4)
]


@app.get("/books")
async def get_all_books():
     return BOOKS

@app.post("/books/create_book")
async def create_book(book_request: BookRequest):
     new_book = Book(**book_request.model_dump())
     BOOKS.append(new_book)
     return {"status": "success", "message": "Book created successfully"}