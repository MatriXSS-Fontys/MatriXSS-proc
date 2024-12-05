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

    # TODO: make screenshot of page content in 'vuln_page_contents' and render in frontend
    # should this be done in JavaScript???

    return jsonify({"page_content": vuln_page_contents}), 200


def get_page_content(url):
    r = requests.get(url)
    return r.text


if __name__ == '__main__':
    app.run(debug=True)
