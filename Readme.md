# FastAPI Learning Projects

This repository contains small projects created while following the Udemy course: [FastAPI - The Complete Course](https://www.udemy.com/course/fastapi-the-complete-course/). Each file represents a self-contained example or a small project from the course.

## Getting Started

To run these projects, you'll need Python 3.8+ installed.

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd fastapi_learn
```

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Running the API Server

You can run any of the project files using `uvicorn`. The command specifies the file name, the FastAPI `app` instance name, and includes the `--reload` flag for auto-reloading during development.

For example, to run the `books.py` project:
```bash
uvicorn BooksApp.books1:app --reload
```
The server will start, typically on `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs` and the alternative documentation at `http://127.0.0.1:8000/redoc`.

---

## Projects Index

1.  **Book Management API (`BooksApp/`)**
    *   `books1.py`: A basic implementation of a book management API.
    *   `books2.py`: A more advanced version with data validation using Pydantic.
2.  **Todo Application (`TodoApp/`)**
    *   A complete to-do list application with a database and user authentication.

---

### Book Management API (`BooksApp/`)

This project demonstrates fundamental FastAPI concepts through two iterations of a book management API.

#### `books1.py`

A simple RESTful API for managing a collection of books. It covers:

*   **Path and Query Parameters:** Fetching data based on URL paths (`/books/id/1`) and query strings (`/books/?category=Science%20Fiction`).
*   **Request Body:** Creating and updating data using `POST` and `PUT` requests.
*   **CRUD Operations:** Implementing Create, Read, Update, and Delete functionalities for the book collection.
*   **In-memory "database":** Uses a simple Python list to store book data for the lifetime of the application instance.

#### `books2.py`

This version enhances the book management API by introducing:

*   **Pydantic Models:** For robust request body validation and data serialization.
*   **Data Classes:** To define the structure of the book data.
*   **Path and Query Validation:** Ensuring that path and query parameters meet specified criteria (e.g., greater than 0).
*   **HTTP Exceptions:** Providing more informative error responses.
*   **Status Codes:** Returning appropriate HTTP status codes for different operations.

### Todo Application (`TodoApp/`)

A full-featured to-do list application that demonstrates a more structured and production-ready approach to building FastAPI applications. Key features include:

*   **Database Integration:** Uses SQLAlchemy to interact with a SQLite database for persistent data storage.
*   **User Authentication:** Implements JWT-based authentication to secure endpoints and manage user sessions.
*   **Password Hashing:** Securely stores user passwords using `passlib`.
*   **API Routers:** Organizes endpoints into separate modules for better code structure (`auth.py` and `todos.py`).
*   **Dependency Injection:** Manages database sessions and user dependencies effectively.
*   **CRUD Operations:** Allows authenticated users to create, read, update, and delete their own to-do items.
*   **Environment Variables:** Manages application secrets and configurations using a `.env` file.
