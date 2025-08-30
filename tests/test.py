import io
import os

import pytest
from app import create_app
from app.configs.errors import API_ERROR_NO_FILE, API_ERROR_INVALID_FILE_TYPE


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_online(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'ok'

def test_validate_pdf_no_file(client):
    response = client.post('/validate')
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == API_ERROR_NO_FILE

def test_validate_pdf_invalid_file_type(client):
    data = {
        'file': (io.BytesIO(b"dummy data"), 'test.txt')
    }
    response = client.post('/validate', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert response.json['status'] == 'error'
    assert response.json['message'] == API_ERROR_INVALID_FILE_TYPE

@pytest.mark.parametrize("folder,expected_validation", [
    ("valid", "pass"),
    ("invalid", "fail")
])

def test_validate_pdf_various(client, folder, expected_validation):
    papers_dir = os.path.join("papers", folder)
    for filename in os.listdir(papers_dir):
        if filename.endswith('.pdf'):
            file_path = os.path.join(papers_dir, filename)
            with open(file_path, 'rb') as f:
                data = {
                    'file': (io.BytesIO(f.read()), filename)
                }
                response = client.post('/validate', data=data, content_type='multipart/form-data')
                assert response.status_code == 200
                assert response.json['status'] == 'success'
                assert response.json['validation'] == expected_validation
                assert 'logs' in response.json


