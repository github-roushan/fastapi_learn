from fastapi import Body, FastAPI, Request

app = FastAPI()

BOOKS = [
  {
    "id": 1,
    "title": "Dune",
    "author": "Frank Herbert",
    "category": "Science Fiction"
  },
  {
    "id": 2,
    "title": "Sapiens: A Brief History of Humankind",
    "author": "Yuval Noah Harari",
    "category": "Non-Fiction, History"
  },
  {
    "id": 3,
    "title": "To Kill a Mockingbird",
    "author": "Harper Lee",
    "category": "Classic Fiction"
  },
  {
    "id": 4,
    "title": "1984",
    "author": "George Orwell",
    "category": "Dystopian, Political Fiction"
  },
  {
    "id": 5,
    "title": "The Name of the Wind",
    "author": "Patrick Rothfuss",
    "category": "Fantasy"
  },
  {
    "id": 6,
    "title": "The Midnight Library",
    "author": "Matt Haig",
    "category": "Contemporary Fiction, Fantasy"
  },
  {
    "id": 7,
    "title": "Educated",
    "author": "Tara Westover",
    "category": "Memoir, Non-Fiction"
  },
  {
    "id": 8,
    "title": "Project Hail Mary",
    "author": "Andy Weir",
    "category": "Science Fiction"
  },
  {
    "id": 9,
    "title": "The Silent Patient",
    "author": "Alex Michaelides",
    "category": "Psychological Thriller"
  },
  {
    "id": 10,
    "title": "The Alchemist",
    "author": "Paulo Coelho",
    "category": "Philosophical Fiction, Adventure"
  },
  {
  "id": 11,
  "title": "Children of Dune",
  "author": "Frank Herbert",
  "category": "Science Fiction"
    }
]

@app.get("/books")
async def get_all_books():
    return BOOKS

@app.get("/books/{category}")
async def get_book_by_category(category: str):
    print("Bad Func", category)
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/get_by/{author}")
async def get_books_by_author(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/{author}/")
async def read_author_category_by_query(author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold() and \
            book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/books/id/{book_id}")
async def get_book_by_id(book_id: int):
    print("Here in book id")
    for book in BOOKS:
        if book.get("id") == book_id:
            return book
    return {"status": 404, "message": "Book not found"}

@app.get("/books/")
async def get_books_by_query(request: Request):
    query_params = request.query_params
    print(query_params.items())
    category = query_params["category"]
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book = Body()):
    print(Body(), new_book)
    BOOKS.append(new_book)
    return {"status": "success", "message": "Book created successfully"}

@app.put("/books/update_book")
async def update_book(updated_book = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == updated_book.get("id"):
            BOOKS[i] = updated_book
    return {"status": "success", "message": "Book updated successfully"}

@app.delete("/books/delete_book/{id}")
async def delete_book(id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == id:
            BOOKS.pop(i)
    return {"status": "success", "message": "Book deleted successfully"}