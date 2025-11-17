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
        // Since we don't have a dedicated endpoint for all URLs, we'll simulate by showing recent ones
        // In a real application, you'd have a proper endpoint for this
        resultDiv.innerHTML = `
            <div class="result info">
                Individual URL operations are working. For a complete list of all URLs, 
                you would need to implement a dedicated endpoint in the backend.
            </div>
        `;
    } catch (error) {
        resultDiv.innerHTML = `<div class="result error">Error: ${error.message}</div>`;
    }
}