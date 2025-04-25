from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

"""
Do this when scraping a website to avoid getting blocked.

headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Accept':
      'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.5',
}

response = requests.get(URL, headers=headers)
"""


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
