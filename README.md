# ⚡ FastAPI Template

A modular, scalable FastAPI starter project designed for fullstack applications and fast prototyping. This template includes a structured layout, database setup with SQLAlchemy, password hashing with bcrypt, and a base for extending with new features.

---

## 📁 Project Structure

```bash
.
├── app  # Contains the main application files.
│   ├── __init__.py   # this file makes "app" a "Python package"
│   ├── main.py       # Initializes the FastAPI application.
│   ├── database.py # Database engine/session setup
│   ├── dependencies.py # Defines dependencies used by the routers
│   ├── routers
│   │   ├── __init__.py
│   │   ├── items.py  # Defines routes and endpoints related to items.
│   │   └── users.py  # Defines routes and endpoints related to users.
│   ├── services
│   │   ├── __init__.py
│   │   ├── item.py  # Defines CRUD operations for items.
│   │   └── user.py  # Defines CRUD operations for users.
│   ├── schemas
│   │   ├── __init__.py
│   │   ├── item.py  # Defines schemas for items.
│   │   └── user.py  # Defines schemas for users.
│   ├── models
│   │   ├── __init__.py
│   │   ├── item.py  # Defines database models for items.
│   │   └── user.py  # Defines database models for users.
│   ├── external_services
│   │   ├── __init__.py
│   │   ├── email.py          # Defines functions for sending emails.
│   │   └── notification.py   # Defines functions for sending notifications
│   └── utils
│       ├── __init__.py
│       ├── authentication.py  # Defines functions for authentication.
│       └── validation.py      # Defines functions for validation.
├── tests
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_items.py  # Tests for the items module.
│   └── test_users.py  # Tests for the users module.
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Features

- ✅ FastAPI with modular project structure
- ✅ SQLAlchemy ORM support
- ✅ SQLite by default, easy to switch to PostgreSQL or others
- ✅ Password hashing with bcrypt
- ✅ Pydantic-based request/response validation
- ✅ Clean separation of concerns (routes, services, models)
- ✅ Environment variable support with `.env`

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/mossi1mj/fastapi-template.git
cd fastapi-template
```
### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file in the root:
```bash
DATABASE_URL=sqlite:///./test.db  # Change to your DB of choice
```
For PostgreSQL:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```
Visit: http://localhost:8000
API Docs: http://localhost:8000/docs

---

## 🧪 Run Tests

To run the test suite:

```bash
pytest
```

---

## Switching Databases
This template is built to work with ***SQL databases*** using ***SQLAlchemy***.

### ✅ Supported SQL Databases
- SQLite (default)
- PostgreSQL
- MySQL (with proper driver installed)

### 🔄 To switch databases:
1. Update your `.env` file with the appropriate `DATABASE_URL`. For example:

```bash
# PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase
```

## ❌ Using NoSQL Databases?

This template is built for SQL databases with SQLAlchemy.

If you want to use a NoSQL database instead, you’ll need to replace the `database.py` logic and bypass SQLAlchemy.

### Recommended NoSQL Options:

| NoSQL DB   | Python Package |
|------------|----------------|
| MongoDB    | `motor` (async), or `pymongo` |
| DynamoDB   | `boto3`         |
| Firestore  | `google-cloud-firestore` |

### How to integrate:

1. **Remove or bypass** SQLAlchemy-based logic in `models/`, `services/`, and `database.py`.
2. **Use native clients** and async/await patterns (especially with FastAPI).
3. Document this change clearly in your own fork for others using the template.

> Example stub code is commented inside `database.py` for non-SQL alternatives.

---

## 🔐 Authentication Notes
- Passwords are hashed using bcrypt in utils/authentication.py.
- Never store passwords in plain text.
- Schema input (UserCreate) expects a raw password.
- The user.py service hashes the password before saving.

You can extend this with:

- JWT Authentication (using python-jose)
- OAuth2 (via Google, Facebook, etc.)

---

## 👤 Author

Made with ❤️ by [Your Name]

If you use this template, feel free to credit or fork it. Contributions are welcome!

[GitHub](https://github.com/mossi1mj) • [LinkedIn](https://linkedin.com/in/mossjmyron)

---

## 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for full details.
