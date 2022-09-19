from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask('')

@app.route('/')

def home():
    return "I'm alive"

def run():
  app.run(host='127.0.0.1',port=os.getenv("PORT") or 3001)


def keep_alive():
    t = Thread(target=run)
    t.start()
