# Converts the repl into a web server
# Which allows the bot to stay alive
# CREDITS TO BEAU FROM FREECODECAMP FOR THIS ONE
# https://www.youtube.com/watch?v=SPTfmiYiuok

from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "<h1>Zero Two Bot Web Server</h1>"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()