from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from jobs import search_berlinstartup, search_web3, search_weworkremotely
app = Flask(__name__)
db = {}
@app.route("/")
def hello_world():
    return render_template("home.html", name="Jennifer")


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
 
    return render_template("search.html", keyword=keyword, jobs_berlinstartup=jobs_berlinstartup, jobs_web3=jobs_web3, jobs_weworkremotely=jobs_weworkremotely)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
