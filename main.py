from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from rq import Queue
from worker import conn

import time
import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

sched = BackgroundScheduler()

q = Queue(connection=conn)

def teste(word):
    print(word)
    
def testeagain(word):
    q.enqueue(teste, word)

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
        sched.add_job(testeagain, trigger=None, args='hello world')
        return {
            "message": "Get Method!"
        }   