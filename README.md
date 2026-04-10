# URL Shortener Service

A lightweight, high-performance URL shortening service built with Flask. This application provides a clean RESTful API alongside a minimal web interface, enabling users to create, manage, and analyze short links with persistent storage via SQLite.

## ✨ Features

- **URL Shortening** — Generate unique, collision-resistant short codes for any valid destination URL.
- **Full CRUD Support** — Create, retrieve, update, and delete short links via RESTful endpoints.
- **Analytics Dashboard** — Track click-through metrics and access counts per link.
- **Seamless Redirection** — Automatic 302 redirection with minimal latency.
- **Input Sanitization** — Comprehensive URL validation to prevent malformed entries.
- **Web Interface** — Clean, responsive frontend for non-technical users.

---

## 🧰 Technology Stack

| Category       | Technology                          |
|----------------|-------------------------------------|
| **Backend**    | Python 3.x, Flask                   |
| **Database**   | SQLite (Development), SQLAlchemy ORM|
| **Validation** | `validators` library                |
| **Frontend**   | HTML5, CSS3, Vanilla JavaScript     |

---

## 📁 Project Structure
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

text

---

## ⚙️ Installation & Setup

### 1. Clone & Environment Setup
```bash
git clone <repository-url>
cd flask-url-shortener
2. Install Dependencies
It is recommended to use a virtual environment.

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
3. Initialize the Database
The application uses SQLite by default. The database schema is automatically created upon the first request or application startup via SQLAlchemy.

4. Run the Application
bash
python app.py
The service will be available at http://localhost:5000.

📡 API Reference
Base URL
http://localhost:5000

Endpoints
Method	Endpoint	Description	Success Response
POST	/shorten	Create a new short URL	201 Created
GET	/<short_code>	Redirect to original URL (increments count)	302 Found
GET	/shorten/<short_code>	Retrieve original URL metadata	200 OK
GET	/shorten/<short_code>/stats	Retrieve access statistics for a short code	200 OK
PUT	/shorten/<short_code>	Update the destination of an existing link	200 OK
DELETE	/shorten/<short_code>	Permanently delete a short URL	204 No Content
GET	/all-urls	List all stored URL mappings (admin only)	200 OK
Example Request: Create Short URL
bash
curl -X POST http://localhost:5000/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/path"}'
Example Response
json
{
  "short_code": "xYz123",
  "short_url": "http://localhost:5000/xYz123",
  "original_url": "https://www.example.com/very/long/path"
}
Example: Get Statistics
bash
curl http://localhost:5000/shorten/xYz123/stats
Response:

json
{
  "short_code": "xYz123",
  "original_url": "https://www.example.com/very/long/path",
  "access_count": 42,
  "created_at": "2026-04-10T10:30:00",
  "updated_at": "2026-04-10T14:22:00"
}
Example: Update URL
bash
curl -X PUT http://localhost:5000/shorten/xYz123 \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.newexample.com"}'
Example: Delete URL
bash
curl -X DELETE http://localhost:5000/shorten/xYz123
🗄️ Data Schema
Column	Type	Constraints	Description
id	INTEGER	PRIMARY KEY, AUTOINCREMENT	Internal record ID
original_url	VARCHAR(2048)	NOT NULL	The full destination URL
short_code	VARCHAR(10)	UNIQUE, NOT NULL	Generated alphanumeric identifier
created_at	DATETIME	DEFAULT CURRENT_TIMESTAMP	Timestamp of creation
updated_at	DATETIME	DEFAULT CURRENT_TIMESTAMP	Timestamp of last modification
access_count	INTEGER	DEFAULT 0	Number of redirects tracked
🛡️ Error Handling
The API returns standard HTTP status codes to indicate the outcome of a request.

Code	Status	Meaning
200	OK	Request succeeded
201	Created	Short URL successfully generated
204	No Content	Delete operation successful
302	Found	Redirecting to original URL
400	Bad Request	Invalid URL supplied or missing JSON payload
404	Not Found	Short code does not exist in the database
500	Internal Server Error	Database connection issue or server exception
🔧 Configuration & Customization
You can modify the application behavior by editing the following variables:

Short Code Length: Adjust the length parameter in the generate_short_code() utility function (default is 6 characters).

Database Engine: To switch from SQLite to PostgreSQL or MySQL, update the SQLALCHEMY_DATABASE_URI configuration string in app.py.

📦 Dependencies
Package	Version	Purpose
Flask	>=2.0.0	Web framework
Flask-SQLAlchemy	>=3.0.0	ORM and database abstraction
validators	>=0.20.0	URL validation utilities
📄 License
This project is open-source and available under the MIT License.
