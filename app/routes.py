from flask import Blueprint, request , jsonify, render_template, send_file, current_app

from app.configs.errors import API_ERROR_NO_FILE, API_ERROR_NO_SELECTED_FILE, API_ERROR_INVALID_FILE_TYPE
from app.services import validator_service
from app.utils import logger

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/ping' , methods=['GET'])
def ping():
    return jsonify({'status' : 'ok' , 'message' : 'ictest-checker'})

import os

@api_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file part"), 400
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No selected file"), 400
        
        if file and file.filename.endswith('.pdf'):
            file_path = f"temp/{file.filename}"
            # Ensure temp dir exists
            os.makedirs("temp", exist_ok=True)
            file.save(file_path)
            
            # Run validation
            logger.Logger.clear_logs()
            is_valid = validator_service.main(file_path, log=True)
            logs = logger.Logger.get_logs()
            
            # The validator saves output to 'rendered_output.pdf' in CWD
            # Rename/Move it to avoid conflicts? Ideally yes, but sticking to simple for now.
            # We will serve it via /download endpoint
            
            return render_template('index.html', 
                                   result='pass' if is_valid else 'fail', 
                                   logs=logs,
                                   download_link="/download/rendered_output.pdf")
            
    return render_template('index.html')

@api_bp.route('/download/<filename>')
def download_file(filename):
    # filename is 'rendered_output.pdf'
    # The validator service saves it in the CWD (project root)
    file_path = os.path.join(os.getcwd(), filename)
    
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return "File not found", 404

@api_bp.route('/validate', methods=['POST'])
def validate_pdf():
    print(request)
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': API_ERROR_NO_FILE}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': API_ERROR_NO_SELECTED_FILE}), 400
    if not file.filename.endswith('.pdf'):
        return jsonify({'status': 'error', 'message': API_ERROR_INVALID_FILE_TYPE}), 400
    file_path = f"temp/{file.filename}"
    file.save(file_path)
    is_valid = validator_service.main(file_path, log=True)
    logs = logger.Logger.get_logs()
    logger.Logger.clear_logs()
    return jsonify({
        'status': 'success',
        'validation': 'pass' if is_valid else 'fail',
        'logs': logs
    }), 200
