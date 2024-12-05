import requests
import os
from flask import Flask, render_template, send_from_directory, request
from models.vulnerability import Vulnerability
from payload import payloads

app = Flask(__name__)

# Path to the exploit.js file for debugging purposes
EXPLOIT_FILE_PATH = os.path.abspath("templates/exploit/exploit.js")

@app.before_request
def before_request():
    # Store the current host in the context for use in templates
    request.current_host = request.host_url

@app.route("/")
def returnExploit():
    # Log the full path for debugging
    print(f"Looking for file at: {EXPLOIT_FILE_PATH}")
    if not os.path.exists(EXPLOIT_FILE_PATH):
        print("File does not exist!")
        return "File not found", 404
    return send_from_directory("templates/exploit", "exploit.js")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard-view.html')

# Functions for XSS payloads


# Define the route for the payloads page
@app.route('/payloads')
def index():
    
    return render_template('payloads-view.jinja', payloads=payloads)

@app.route("/results")
def found_vulns_page():
    found_vulns = [Vulnerability('https://example.com', '#username', '/')]
    return render_template('results-view.jinja', found_vulns=found_vulns)

# Function to send a request and fetch page title (for scraping or other purposes)
def send_request():
    r = requests.get("https://example.com/")
    content = r.text
    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title
    print("page title: " + title.text)

if __name__ == '__main__':
    app.run(debug=True)
