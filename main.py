import requests
import models.vulnerability
from bs4 import BeautifulSoup
from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader
from flask import Flask, send_from_directory
from models.vulnerability import Vulnerability

env = Environment(loader = FileSystemLoader('templates'))
app = Flask(__name__)
import os
print(os.path.abspath('static/exploit.js'))
@app.route("/")
def hello_world():  
    return send_from_directory('exploit', 'exploit.js')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard-view.html')

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
    app.run(debug=True)
