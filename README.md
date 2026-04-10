# URL Shortener

A lightweight, high-performance URL shortening service built with Flask. This application provides a clean RESTful API alongside a minimal web interface, enabling users to create, manage, and analyze short links with persistent storage via SQLite.

## Features

- **URL Shortening** — Generate unique, collision-resistant short codes for any valid destination URL.
- **Full CRUD Support** — Create, retrieve, update, and delete short links via RESTful endpoints.
- **Analytics Dashboard** — Track click-through metrics and access counts per link.
- **Seamless Redirection** — Automatic `302` redirection with minimal latency.
- **Input Sanitization** — Comprehensive URL validation to prevent malformed entries.
- **Web Interface** — Clean, responsive frontend for non-technical users.

---

## Technology Stack

| Category       | Technology                          |
| :------------- | :---------------------------------- |
| **Backend**    | Python 3.x, Flask                   |
| **Database**   | SQLite (Development), SQLAlchemy ORM|
| **Validation** | `validators` library                |
| **Frontend**   | HTML5, CSS3, Vanilla JavaScript     |

---

## Project Structure
```
flask-url-shortener/
├── app.py # Application factory & server entry point
├── models.py # SQLAlchemy data models & schema definition
├── routes.py # Blueprint route handlers & API logic
├── requirements.txt # Dependency manifest
├── init.py # Package initializer
├── templates/
│ └── index.html # Main user interface template
└── static/
├── style.css # Custom styling
└── script.js # Client-side interaction logic
```

---

## ⚙️ Installation & Setup

### 1. Clone & Environment Setup
```bash
git clone <repository-url>
cd flask-url-shortener
```
```
2. Install Dependencies
It is recommended to use a virtual environment.

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
```
3. Initialize the Database
The application uses SQLite by default. The database schema is automatically created upon the first request or application startup via SQLAlchemy.
```
```
4. Run the Application
bash
python app.py
The service will be available at http://localhost:5000.
```
---

## Dependencies
Flask — Micro web framework.
Flask-SQLAlchemy — ORM for database abstraction.
validators — Strict URL validation logic.
