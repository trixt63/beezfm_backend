# Hotels Management System

A backend API for hotel management built with FastAPI and Python.

## Quick Start

1. Clone the repository and navigate to the project directory
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file based on the example below
4. Run the application: `python3 main.py`
5. Access the API at `http://localhost:8000`
6. View API documentation at `http://localhost:8000/docs`

## Requirements

- Python 3.6+
- PostgreSQL
- FastAPI

## Environment Variables

Create a `.env` file with the following:
```
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/postgres
API_HOST="0.0.0.0"
API_PORT=8000
```