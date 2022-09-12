# Converts the repl into a web server
# Which allows the bot to stay alive
# CREDITS TO BEAU FROM FREECODECAMP FOR THIS ONE
# https://www.youtube.com/watch?v=SPTfmiYiuok

from flask import Flask
from threading import Thread

app = Flask("")

@app.route("/")
def home():
    return "<h1>Cosette Bot is alive</h1>"

def run():
    app.run(host='localhost', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()