from flask import Flask, request, json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'