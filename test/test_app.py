import os
import tempfile
import pytest
from flask import url_for
from build.app import app, db, User, Document
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    client = app.test_client()
    with app.app_context():
        db.create_all()
        # Seed users
        alice = User(id=1, username='alice', password_hash=generate_password_hash('alicepass'))
        bob = User(id=2, username='bob', password_hash=generate_password_hash('bobpass'))
        db.session.add_all([alice, bob])
        # Seed document for bob (id=42)
        doc = Document(id=42, user_id=2, filename='confidential-bob.pdf', filepath=os.path.join(os.path.dirname(__file__), '../build/uploads/confidential-bob.pdf'))
        db.session.add(doc)
        db.session.commit()
    yield client
    os.close(db_fd)
    os.unlink(db_path)

def login(client, username, password):
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)

def test_register_and_login(client):
    rv = client.post('/register', data={'username': 'newuser', 'password': 'newpass'}, follow_redirects=True)
    assert b'Registration successful' in rv.data
    rv = login(client, 'newuser', 'newpass')
    assert b'My Documents' in rv.data

def test_upload_and_list_document(client):
    login(client, 'alice', 'alicepass')
    data = {
        'file': (open(os.path.join(os.path.dirname(__file__), '../build/uploads/confidential-bob.pdf'), 'rb'), 'test.pdf')
    }
    rv = client.post('/lab', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert b'Document uploaded successfully' in rv.data
    rv = client.get('/lab')
    assert b'test.pdf' in rv.data

def test_idor_download(client):
    login(client, 'alice', 'alicepass')
    rv = client.get('/download/42')
    assert rv.status_code == 200
    assert b'dummy' in rv.data  # contenu du PDF seedé
    # Alice ne devrait pas posséder ce document, mais peut le télécharger (IDOR) 