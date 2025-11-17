from flask import Flask, request, jsonify, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import string
import random
import validators
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Model definition
class ShortURL(db.Model):
    __tablename__ = 'short_urls'
    
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), 
                          onupdate=lambda: datetime.now(timezone.utc))
    access_count = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.original_url,
            'shortCode': self.short_code,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
            'accessCount': self.access_count
        }
    
    def __repr__(self):
        return f'<ShortURL {self.short_code} -> {self.original_url}>'

# Utility functions
def generate_short_code(length=6):
    """Generate a random short code"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def validate_url(url):
    """Validate URL format"""
    if not url:
        return False, "URL is required"
    
    if not validators.url(url):
        return False, "Invalid URL format"
    
    return True, ""

# Create database tables
with app.app_context():
    db.create_all()

# API Routes
@app.route('/shorten', methods=['POST'])
def create_short_url():
    """Create a new short URL"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    url = data['url']
    
    # Validate URL
    is_valid, error_message = validate_url(url)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    # Generate unique short code
    short_code = generate_short_code()
    while ShortURL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()
    
    # Create new short URL
    new_url = ShortURL(original_url=url, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    
    return jsonify(new_url.to_dict()), 201

@app.route('/shorten/<short_code>', methods=['GET'])
def get_short_url(short_code):
    """Retrieve original URL from short code"""
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not short_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    return jsonify(short_url.to_dict()), 200

@app.route('/<short_code>')
def redirect_to_original(short_code):
    """Redirect to original URL and track access count"""
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not short_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    # Increment access count
    short_url.access_count += 1
    db.session.commit()
    
    return redirect(short_url.original_url)

@app.route('/shorten/<short_code>', methods=['PUT'])
def update_short_url(short_code):
    """Update an existing short URL"""
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not short_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    new_url = data['url']
    
    # Validate URL
    is_valid, error_message = validate_url(new_url)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    
    # Update URL
    short_url.original_url = new_url
    db.session.commit()
    
    return jsonify(short_url.to_dict()), 200

@app.route('/shorten/<short_code>', methods=['DELETE'])
def delete_short_url(short_code):
    """Delete a short URL"""
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not short_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    db.session.delete(short_url)
    db.session.commit()
    
    return '', 204

@app.route('/shorten/<short_code>/stats', methods=['GET'])
def get_url_stats(short_code):
    """Get statistics for a short URL"""
    short_url = ShortURL.query.filter_by(short_code=short_code).first()
    
    if not short_url:
        return jsonify({'error': 'Short URL not found'}), 404
    
    return jsonify(short_url.to_dict()), 200

@app.route('/all-urls', methods=['GET'])
def get_all_urls():
    """Get all short URLs (for frontend display)"""
    urls = ShortURL.query.all()
    return jsonify([url.to_dict() for url in urls])

# Frontend Routes
@app.route('/')
def index():
    """Frontend interface"""
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>URL Shortener</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #333;
                background-color: #f4f4f4;
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
                color: #2c3e50;
            }
            .section {
                margin-bottom: 30px;
                padding: 20px;
                border: 1px solid #e1e1e1;
                border-radius: 8px;
                background: #fafafa;
            }
            .section h2 {
                margin-bottom: 15px;
                color: #34495e;
                font-size: 1.2em;
            }
            form {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                flex-wrap: wrap;
            }
            input[type="url"], input[type="text"] {
                flex: 1;
                min-width: 200px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            button {
                padding: 10px 20px;
                background: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 14px;
                transition: background 0.3s;
            }
            button:hover {
                background: #2980b9;
            }
            button.danger {
                background: #e74c3c;
            }
            button.danger:hover {
                background: #c0392b;
            }
            .result {
                padding: 10px;
                margin-top: 10px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 14px;
                white-space: pre-wrap;
                word-break: break-all;
            }
            .success {
                background: #d4edda;
                border: 1px solid #c3e6cb;
                color: #155724;
            }
            .error {
                background: #f8d7da;
                border: 1px solid #f5c6cb;
                color: #721c24;
            }
            .info {
                background: #d1ecf1;
                border: 1px solid #bee5eb;
                color: #0c5460;
            }
            .url-item {
                padding: 10px;
                margin: 5px 0;
                background: white;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            .url-item:hover {
                background: #f8f9fa;
            }
            @media (max-width: 600px) {
                form {
                    flex-direction: column;
                }
                input[type="url"], input[type="text"] {
                    min-width: 100%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>URL Shortener</h1>
            
            <!-- Create Short URL Form -->
            <div class="section">
                <h2>Create Short URL</h2>
                <form id="createForm">
                    <input type="url" id="originalUrl" placeholder="Enter your long URL" required>
                    <button type="submit">Shorten URL</button>
                </form>
                <div id="createResult"></div>
            </div>

            <!-- Get URL Form -->
            <div class="section">
                <h2>Get Original URL</h2>
                <form id="getForm">
                    <input type="text" id="shortCodeGet" placeholder="Enter short code" required>
                    <button type="submit">Get URL</button>
                </form>
                <div id="getResult"></div>
            </div>

            <!-- Update URL Form -->
            <div class="section">
                <h2>Update Short URL</h2>
                <form id="updateForm">
                    <input type="text" id="shortCodeUpdate" placeholder="Short code" required>
                    <input type="url" id="newUrl" placeholder="New URL" required>
                    <button type="submit">Update URL</button>
                </form>
                <div id="updateResult"></div>
            </div>

            <!-- Delete URL Form -->
            <div class="section">
                <h2>Delete Short URL</h2>
                <form id="deleteForm">
                    <input type="text" id="shortCodeDelete" placeholder="Enter short code" required>
                    <button type="submit" class="danger">Delete URL</button>
                </form>
                <div id="deleteResult"></div>
            </div>

            <!-- Get Stats Form -->
            <div class="section">
                <h2>Get URL Statistics</h2>
                <form id="statsForm">
                    <input type="text" id="shortCodeStats" placeholder="Enter short code" required>
                    <button type="submit">Get Stats</button>
                </form>
                <div id="statsResult"></div>
            </div>

            <!-- All URLs Section -->
            <div class="section">
                <h2>All Short URLs</h2>
                <button onclick="loadAllURLs()">Load All URLs</button>
                <div id="allUrls"></div>
            </div>
        </div>

        <script>
            const API_BASE = '';

            // Create Short URL
            document.getElementById('createForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const url = document.getElementById('originalUrl').value;
                const resultDiv = document.getElementById('createResult');
                
                try {
                    const response = await fetch('/shorten', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <strong>Short URL created successfully!</strong><br>
                                Short Code: ${data.shortCode}<br>
                                Original URL: ${data.url}<br>
                                Access your short URL: <a href="/${data.shortCode}" target="_blank">/${data.shortCode}</a>
                            </div>
                        `;
                        document.getElementById('createForm').reset();
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Network error: ${error.message}</div>`;
                }
            });

            // Get Original URL
            document.getElementById('getForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const shortCode = document.getElementById('shortCodeGet').value;
                const resultDiv = document.getElementById('getResult');
                
                try {
                    const response = await fetch(`/shorten/${shortCode}`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <strong>URL Found!</strong><br>
                                Short Code: ${data.shortCode}<br>
                                Original URL: ${data.url}<br>
                                Created: ${new Date(data.createdAt).toLocaleString()}<br>
                                <a href="${data.url}" target="_blank">Visit URL</a>
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Network error: ${error.message}</div>`;
                }
            });

            // Update Short URL
            document.getElementById('updateForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const shortCode = document.getElementById('shortCodeUpdate').value;
                const newUrl = document.getElementById('newUrl').value;
                const resultDiv = document.getElementById('updateResult');
                
                try {
                    const response = await fetch(`/shorten/${shortCode}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ url: newUrl })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <strong>URL updated successfully!</strong><br>
                                Short Code: ${data.shortCode}<br>
                                New URL: ${data.url}<br>
                                Updated: ${new Date(data.updatedAt).toLocaleString()}
                            </div>
                        `;
                        document.getElementById('updateForm').reset();
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Network error: ${error.message}</div>`;
                }
            });

            // Delete Short URL
            document.getElementById('deleteForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const shortCode = document.getElementById('shortCodeDelete').value;
                const resultDiv = document.getElementById('deleteResult');
                
                try {
                    const response = await fetch(`/shorten/${shortCode}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.status === 204) {
                        resultDiv.innerHTML = `<div class="result success">Short URL "${shortCode}" deleted successfully!</div>`;
                        document.getElementById('deleteForm').reset();
                    } else {
                        const data = await response.json();
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Network error: ${error.message}</div>`;
                }
            });

            // Get URL Statistics
            document.getElementById('statsForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const shortCode = document.getElementById('shortCodeStats').value;
                const resultDiv = document.getElementById('statsResult');
                
                try {
                    const response = await fetch(`/shorten/${shortCode}/stats`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `
                            <div class="result success">
                                <strong>Statistics for ${data.shortCode}</strong><br>
                                Original URL: ${data.url}<br>
                                Access Count: ${data.accessCount}<br>
                                Created: ${new Date(data.createdAt).toLocaleString()}<br>
                                Last Updated: ${new Date(data.updatedAt).toLocaleString()}
                            </div>
                        `;
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Network error: ${error.message}</div>`;
                }
            });

            // Load all URLs
            async function loadAllURLs() {
                const resultDiv = document.getElementById('allUrls');
                resultDiv.innerHTML = '<div class="result info">Loading...</div>';
                
                try {
                    const response = await fetch('/all-urls');
                    const data = await response.json();
                    
                    if (response.ok) {
                        if (data.length === 0) {
                            resultDiv.innerHTML = '<div class="result info">No URLs found. Create your first short URL!</div>';
                            return;
                        }
                        
                        let html = '<div class="result success">';
                        data.forEach(url => {
                            html += `
                                <div class="url-item">
                                    <strong>${url.shortCode}</strong><br>
                                    Original: ${url.url}<br>
                                    Access Count: ${url.accessCount}<br>
                                    Created: ${new Date(url.createdAt).toLocaleString()}<br>
                                    <a href="/${url.shortCode}" target="_blank">Visit</a> | 
                                    <a href="/shorten/${url.shortCode}/stats" target="_blank">Stats</a>
                                </div>
                            `;
                        });
                        html += '</div>';
                        resultDiv.innerHTML = html;
                    } else {
                        resultDiv.innerHTML = `<div class="result error">Error: ${data.error}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)