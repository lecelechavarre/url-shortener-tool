# URL Shortener Service

A simple and efficient URL shortener service built with Flask that
allows you to create, manage, and track short URLs with a clean RESTful
API and web interface.

## 🚀 Features

-   **Create Short URLs** -- Generate unique short codes for long URLs\
-   **Retrieve Original URLs** -- Get original URL from short code\
-   **Update Short URLs** -- Modify destination URLs\
-   **Delete Short URLs** -- Remove unwanted short URLs\
-   **Access Statistics** -- Track click counts for each short URL\
-   **Automatic Redirects** -- Seamless redirection\
-   **RESTful API** -- Clean API endpoints\
-   **Web Interface** -- User-friendly frontend\
-   **URL Validation** -- Ensures valid URL formats

------------------------------------------------------------------------

## 🧰 Tech Stack

**Backend:** Python Flask\
**Database:** SQLite + SQLAlchemy ORM\
**Frontend:** HTML, CSS, JavaScript\
**Validation:** `validators` library

------------------------------------------------------------------------

## 📁 Project Structure

    flask-url-shortener/
    │
    ├── app.py                 # Main application factory
    ├── models.py              # Database models
    ├── routes.py              # API routes and handlers
    ├── requirements.txt       # Project dependencies
    ├── __init__.py           # Package initialization
    │
    ├── templates/
    │   └── index.html        # Main frontend template
    │
    └── static/
        ├── style.css         # CSS stylesheets
        └── script.js         # Frontend JavaScript

------------------------------------------------------------------------

## 🔧 Installation

### 1. Create project directory

``` bash
mkdir flask-url-shortener
cd flask-url-shortener
```

### 2. Create folders

``` bash
mkdir templates static
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Running the Application

Start the server:

``` bash
python app.py
```

Access the app: - **Web:** http://localhost:5000\
- **API Base URL:** http://localhost:5000

------------------------------------------------------------------------

## 📡 API Endpoints

### **Create Short URL**

    POST /shorten
    Content-Type: application/json
    {
      "url": "https://www.example.com/some/long/url"
    }

### **Retrieve Original URL**

    GET /shorten/{short_code}

### **Redirect**

    GET /{short_code}

### **Update Short URL**

    PUT /shorten/{short_code}

### **Delete Short URL**

    DELETE /shorten/{short_code}

### **Statistics**

    GET /shorten/{short_code}/stats

### **Get All URLs**

    GET /all-urls

------------------------------------------------------------------------

## 🔍 Usage Examples

### **Create URL**

``` bash
curl -X POST http://localhost:5000/shorten -H "Content-Type: application/json" -d '{"url": "https://www.example.com"}'
```

### **Redirect**

``` bash
curl -L http://localhost:5000/abc123
```

### **Get Stats**

``` bash
curl http://localhost:5000/shorten/abc123/stats
```

### **Update**

``` bash
curl -X PUT http://localhost:5000/shorten/abc123 -H "Content-Type: application/json" -d '{"url": "https://www.newexample.com"}'
```

### **Delete**

``` bash
curl -X DELETE http://localhost:5000/shorten/abc123
```

------------------------------------------------------------------------

## 🗄️ Database Schema

    CREATE TABLE short_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        original_url VARCHAR(2048) NOT NULL,
        short_code VARCHAR(10) UNIQUE NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        access_count INTEGER DEFAULT 0
    );

------------------------------------------------------------------------

## ⚠️ Error Handling

-   **200 OK**
-   **201 Created**
-   **204 No Content**
-   **400 Bad Request**
-   **404 Not Found**

------------------------------------------------------------------------

## 🛠 Development Notes

### Adding Endpoints

1.  Add route in `routes.py`\
2.  Implement handler\
3.  Update frontend if needed

### Database Changes

Edit `models.py` → DB auto-updates

------------------------------------------------------------------------

## 🎨 Customization

-   **Short code length:** adjust in `generate_short_code()`\
-   **Database engine:** change `SQLALCHEMY_DATABASE_URI`\
-   **Styles:** edit `static/style.css`

------------------------------------------------------------------------

## 📦 Dependencies

-   Flask\
-   Flask-SQLAlchemy\
-   Validators
