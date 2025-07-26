from flask import Flask, request

import checker
from utils.logger import Logger

app = Flask(__name__)

@app.route('/')
def ping():
    return 'ictest-checker'

@app.route('/check')
def check():
    val = str(checker.check("papers/valid/1.pdf"))
    return val
from flask import jsonify

@app.route('/checkpdf', methods=['POST'])
def check_pdf():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and file.filename.endswith('.pdf'):
        file_path = f"temp/{file.filename}"
        file.save(file_path)
        result = checker.check(file_path)
        copy_logs = Logger.get_logs()
        Logger.clear_logs()
        return jsonify({
            "status": result,
            "logs": copy_logs
        }), 200
    else:
        return "Invalid file type", 400
