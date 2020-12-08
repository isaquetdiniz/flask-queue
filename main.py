import sys
import logging
import json
import requests

from flask import Flask, request, make_response, render_template
from rq import Queue
from worker import conn
from scrapings import magazine_luiza
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
q = Queue(connection=conn)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
sched = BackgroundScheduler()
sched.start()

def scraping(link):
  data = magazine_luiza.parse(link, 'magazine_luiza')

  headers = { 'Authorization': 'Bearer ' }
  requests.post(
    '',
    params={ "data": json.dumps(data), "link": link },
    headers=headers
  )

def run_queue_scraping(links):
  for link in links:
    q.enqueue(scraping, link)

@app.route('/register', methods=['POST'])
def link_products():
  try:
    data = request.get_json()

    sched.add_job(run_queue_scraping, args=[data['links_products']])
    return "Done"
  except Exception as err:
    print(f"Error: {err}")
