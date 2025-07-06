from flask import Flask

import checker

app = Flask(__name__)

@app.route('/')
def ping():
    return 'ictest-checker'

@app.route('/check')
def check():
    val = checker.check("papers/valid/1.pdf")
    return val
