from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from jobs import search_berlinstartup, search_web3, search_weworkremotely
import os
import subprocess
import sys

app = Flask(__name__)
db = {}

# Install Playwright browsers if not already installed
def install_playwright():
    try:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        subprocess.run([sys.executable, "-m", "playwright", "install-deps"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing Playwright: {e}")
        # Continue anyway, we'll handle the error in the actual usage

# Install Playwright on startup
install_playwright()


@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword in db:
        jobs_berlinstartup = db[keyword]["jobs_berlinstartup"]
        jobs_web3 = db[keyword]["jobs_web3"]
        jobs_weworkremotely = db[keyword]["jobs_weworkremotely"]
    else:
        jobs_berlinstartup = search_berlinstartup(keyword)
        jobs_web3 = search_web3(keyword)
        jobs_weworkremotely = search_weworkremotely(keyword)
        db[keyword] = {
            "jobs_berlinstartup": jobs_berlinstartup,
            "jobs_web3": jobs_web3,
            "jobs_weworkremotely": jobs_weworkremotely
        }
    jobs_weworkremotely = []
    return render_template("search.html", keyword=keyword, jobs_berlinstartup=jobs_berlinstartup, jobs_web3=jobs_web3, jobs_weworkremotely=jobs_weworkremotely)

@app.route("/")
def hello_world():
    return render_template("home.html", name="Jennifer")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
