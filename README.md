# 🎓 School & Student Management API

A simple **FastAPI** project for managing **Schools** and **Students** using  
**Async SQLAlchemy** and **SQLite**.

This project is built for learning purposes and demonstrates:
- Async CRUD operations
- One-to-Many relationships (School ➜ Students)
- Clean project structure
- Pydantic schemas (Pydantic v2)



## Tech Stack

- **FastAPI**
- **SQLAlchemy (Async)**
- **SQLite**
- **Pydantic v2**
- **Uvicorn**


##  Installation & Setup

### 1- Create virtual environment
```bash
python -m venv .venv
```

### 2- Activate virtual environment
```bash
.venv\Scripts\activate
```
### 3- Install dependencies
```bash
pip install -r requirements.txt
```
### 4- Run the Project
```bash
uvicorn main:app --reload
```
# School Endpoints
| Method | Endpoint | Description |
|------|--------|------------|
| POST | `/school/` | Add new school |
| GET | `/school/` | Get all schools |
| GET | `/school/{id}` | Get school by ID |
| GET | `/school/{id}/students` | Get school with students |
| DELETE | `/school/{id}` | Delete school |


Example – Create School
```json
{
  "name": "An-Najah National University",
  "founding_date": "1977-01-01T00:00:00",
  "address": "New Campus",
  "city": "Nablus"
}
```


# Student Endpoints
| Method | Endpoint | Description |
|------|--------|------------|
| POST | `/student/` | Add student|
| GET | `/student/{id}` | Get student by ID |
| GET | `/student/{id}` | Update student |
| DELETE | `/student/{id}` | Delete student |

Example – Create Student
```json
{
  "first_name": "Sara",
  "last_name": "Ahmad",
  "birth_date": "2003-05-10T00:00:00",
  "school_id": 1
}
```

# Data Validation

A student cannot be added unless the school exists.

Proper HTTP status codes are returned (404, 200, 201).

# Learning Goals

This project helps understand:

 - Async programming in FastAPI

 - SQLAlchemy relationships

 - CRUD operations

 - Clean API design

 - Pydantic schemas & validation




