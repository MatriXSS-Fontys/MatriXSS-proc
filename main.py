import requests
import models.vulnerability
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify
from jinja2 import Environment, FileSystemLoader

from models.vulnerability import Vulnerability

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.jinja')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard-view.html')

@app.route("/results")
def found_vulns_page():
    found_vulns = [Vulnerability('https://example.com', '#username', '/')]
    return render_template('results-view.jinja', found_vulns=found_vulns)

@app.route("/capture-data", methods=['POST'])
def capture_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON data received"}), 400

    url = data.get('url')
    element_selector = data.get('element_selector')
    page_name = data.get('page_name')

    if not all([url, element_selector, page_name]):
        return jsonify({"error": "Missing required fields"}), 400

    print(f"Received data: URL={url}, Selector={element_selector}, Page Name={page_name}")

    return jsonify({"message": "Data received successfully", "received": data}), 200


def send_request():
    r = requests.get("https://example.com/")
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title

    print("page title: " + title.text)


if __name__ == '__main__':
    app.run(debug=True)
