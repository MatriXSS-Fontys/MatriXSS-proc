import requests
import logging
import models.vulnerability
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from jinja2 import Environment, FileSystemLoader
from flask import Flask, send_from_directory, request, render_template_string
from models.vulnerability import Vulnerability

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)
import os
print(os.path.abspath('static/exploit.js'))
from flask import Flask, send_from_directory, request, session, redirect, url_for, abort
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session handling
logging.basicConfig(level=logging.INFO)

# Default to 'exploit.js' for all users until changed via admin
@app.route("/", methods=["GET"])
def serve_file():
    # Get the currently selected file from the session (default is 'exploit.js')
    current_file = session.get("current_file", "exploit.js")

    # Define the path to the requested file
    base_directory = os.path.abspath("templates/exploit") 
    file_path = os.path.join(base_directory, current_file)
    # Security: Prevent directory traversal
    if not file_path.startswith(base_directory):
        abort(403)  # Forbidden

    # Check if the file exists
    if not os.path.exists(file_path):
        return "File not found", 404

    # Serve the selected file
    return send_from_directory(base_directory, current_file)

@app.route("/home", methods=["GET"])
def home_page():
    return render_template("home.jinja")

@app.route("/SelectExploit", methods=["GET", "POST"])
def admin_page():
    base_directory = os.path.abspath("templates/exploit") 
    # If the request method is POST, update the file to be served
    if request.method == "POST":
        # Get the new file from the form data
        new_file = request.form.get("file")
        if new_file:
            # Update the session to store the current file
            session["current_file"] = new_file
            return redirect(url_for("admin_page"))

    # List all files in the exploit folder
    available_files = [f for f in os.listdir(base_directory) if os.path.isfile(os.path.join(base_directory, f))]

    # Render the admin page with the list of available files
    return render_template("SelectExploit.html", available_files=available_files, current_file=session.get("current_file", "exploit.js"))



@app.route("/dashboard")
def dashboard():
    return render_template('dashboard-view.html')

@app.route("/results")
def found_vulns_page():
    found_vulns = [
        Vulnerability('https://example.com', '#example', '/example'),
        Vulnerability('https://github.com', '#example', '/example'),
    ]
    return render_template('results-view.html', found_vulns=found_vulns)

@app.route("/handle-vuln-data", methods=['POST'])
def handle_vuln_data():
    """
    Gets the vulnerable page HTML by using `requests`. This is used to be able to display a preview of the vulnerable website.
    This function might later on be (partially) replaced by html2canvas.js.
    :return:
    A string with the HTML contents of the vulnerable page that was requested.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    url = data.get('url')
    element_selector = data.get('element_selector')
    page_name = data.get('page_name')
    
    if not all([url, element_selector, page_name]):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Get the HTML contents from the vulnerable page for displaying in frontend
    vulnerability = Vulnerability(url, element_selector, page_name)
    vuln_page_contents = get_page_content(url)
    
    return jsonify({"page_content": vuln_page_contents}), 200

@app.route("/exploitselect")
def select_exploit_page():
    return render_template("exploitSelect.html")

@app.route('/callback', methods=['POST'])
def handle_callback():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid JSON'}), 400

    app.logger.info(f"Received callback: {data}")

    event = data.get('event')
    location = data.get('location')
    timestamp = data.get('timestamp')

    print(f"Event: {event}")
    print(f"Location: {location}")
    print(f"Timestamp: {timestamp}")

    return jsonify({'status': 'Callback received'}), 200


def get_page_content(url):
    r = requests.get(url)
    return r.text

if __name__ == '__main__':
    app.run(debug=True)
