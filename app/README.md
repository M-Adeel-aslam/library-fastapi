
# LibraryAPI

A FastAPI-based backend system where users can register, log in, publish literary or artistic works, and support other users’ works with transactions.

## Features

- User authentication (JWT-based)
- Users can create, view, update, and delete their own works
- Public listing and detail view of works
- Support system where users can financially support works
- Secure password hashing using Passlib
- Relationship-driven data model (Users ↔ Works ↔ Support)
- PostgreSQL database with SQLAlchemy ORM

## Technologies Used

- **Python 3.9+**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **JWT (PyJWT)**
- **Passlib (bcrypt)**
- **Uvicorn**

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/library-api.git
cd library-api
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://user:password@localhost:5432/librarydb
KEY=your-secret-key
ALGORITHM=HS256
EXPIRE_TOKEN_TIME=30
```

### 5. Run the App

```bash
uvicorn app.main:app --reload
```

Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive API documentation.

## Project Structure

```
library-api/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schema.py
│   ├── database.py
│   ├── auth.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── works.py
│   │   ├── support.py
│   └── utils.py
│
├── requirements.txt
├── .env
└── README.md
```

## API Endpoints

### Auth (Public)
- `POST /register` → user registration
- `POST /login` → obtain JWT token

### Works (Protected)
- `POST /works`
- `GET /works`
- `GET /works/{id}`
- `PUT /works/{id}`
- `DELETE /works/{id}`

### Support (Protected)
- `POST /works/{id}/support`
- `GET /works/{id}/support`
- `GET /users/{id}/support`

