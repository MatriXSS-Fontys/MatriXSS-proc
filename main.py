import requests
from bs4 import BeautifulSoup
from flask import Flask
from jinja2 import Environment, FileSystemLoader

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/found-vulns")
def found_vulns_page():
    template = env.get_template('results-view.html')
    page_content = template.render(custom_element='<h1>epic developer time</h1>')
    return page_content



def send_request():
    r = requests.get("https://example.com/")
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title
    print("page title: " + title.text)
