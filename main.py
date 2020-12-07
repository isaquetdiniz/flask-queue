from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from rq import Queue
from worker import conn
import sys
import logging

from scrapins import magazine_luiza

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
sched = BackgroundScheduler()

q = Queue(connection=conn)

def scraping(link):
    print(magazine_luiza.parse(link, 'margazine_luiza'))
    
def run_scraping(links):
    for link in links:
        q.enqueue(scraping, link)

sched.start()

app = Flask(__name__)

@app.route('/')
def hello_message():
    return {
        "App": "microservice-python",
        "Status": "develop",
        "Author": "Isaque Diniz"
    }

@app.route('/methods', methods=['GET', 'POST'])
def link_products():
    if request.method == 'POST':
        return  {
            "message": "Post Method"
        }
    else:
        data = request.get_json()
        sched.add_job(run_scraping, trigger=None, args=[data['links_products']])
        return {
            "message": "Get Method!"
        }   