import requests
from bs4 import BeautifulSoup


if __name__ == '__main__':
    r = requests.get("https://example.com/")
    content = r.text

    soup = BeautifulSoup(content, 'html.parser')
    title = soup.title
    print("page title: " + title.text)
