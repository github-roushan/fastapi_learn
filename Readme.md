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

Install the required Python packages, FastAPI for the framework and Uvicorn to run the server.

```bash
pip install fastapi "uvicorn[standard]"
```

### 4. Running the API Server

You can run any of the project files using `uvicorn`. The command specifies the file name, the FastAPI `app` instance name, and includes the `--reload` flag for auto-reloading during development.

For example, to run the `books.py` project:
```bash
uvicorn books:app --reload
```
The server will start, typically on `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs` and the alternative documentation at `http://127.0.0.1:8000/redoc`.

---

## Projects Index

1.  Book Management API (`books.py`)

---

### Book Management API (`books.py`)

This project is a simple RESTful API for managing a collection of books. It demonstrates fundamental FastAPI concepts including:

*   **Path and Query Parameters:** Fetching data based on URL paths (`/books/id/1`) and query strings (`/books/?category=Science%20Fiction`).
*   **Request Body:** Creating and updating data using `POST` and `PUT` requests.
*   **CRUD Operations:** Implementing Create, Read, Update, and Delete functionalities for the book collection.
*   **In-memory "database":** Uses a simple Python list to store book data for the lifetime of the application instance.
