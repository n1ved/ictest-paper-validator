from flask import Blueprint, request , jsonify
from app.services import validator_service
from app.utils import logger

api_bp = Blueprint('api', __name__)

@api_bp.route('/' , methods=['GET'])
def ping():
    return jsonify({'status' : 'ok' , 'message' : 'ictest-checker'})

@api_bp.route('/validate', methods=['POST'])
def validate_pdf():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'Request does not contain any files'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400
    if not file.filename.endswith('.pdf'):
        return jsonify({'status': 'error', 'message': 'Invalid file type, only PDF allowed'}), 400
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
