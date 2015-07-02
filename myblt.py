import os
import hashlib
import binascii
import string, random
import mimetypes
import uuid

from flask import Flask, request, send_from_directory, jsonify, redirect
from database import db_session, init_db
from models import Upload, User

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['API_URL'] = 'http://a.myb.lt/'


def hash_exists(hash):
    return Upload.query.filter(Upload.hash == hash).count() != 0

def short_url_exists(url):
    if not url:
        return True
    return Upload.query.filter(Upload.short_url == url).count() != 0

def get_random_short_url():
    """Generates a random string of 7 ascii letters and digits
    Can provide in the order or 10^12 unique strings
    """
    pool = string.ascii_letters + string.digits
    return ''.join(random.choice(pool) for _ in range(7))

def get_new_short_url():
    """Generate random urls until a new one is generated"""
    url = None
    while short_url_exists(url):
        url = get_random_short_url()
    return url

def new_user(username, password):
    # TODO generate new salt with every user
    salt = "salty"
    hashpass = get_hash(password, salt)

    user = User(username, hashpass, salt)
    db_session.add(user)
    db_session.commit()

    return user

def get_hash(password, salt):
    m = hashlib.sha512()
    m.update(salt.encode('utf8'))
    m.update(password.encode('utf8'))
    return m.digest()

def get_auth_error():
    token = request.cookies.get('token')
    if not token:
        return jsonify({'error': 'Unauthorized'}), 403
    user = User.query.filter(User.token == token).first()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return BadRequest

    # Get sha1 of uploaded file
    m = hashlib.sha1()
    m.update(file.read())
    file_hash_bin = m.digest()

    if not hash_exists(file_hash_bin):
        # Save new file to uploads folder
        file_hash_str = str(binascii.hexlify(file_hash_bin).decode('utf8'))
        abs_file = os.path.join(app.config['UPLOAD_FOLDER'], file_hash_str)
        extension = mimetypes.guess_extension(file.mimetype)

        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        file.stream.seek(0)
        file.save(abs_file)

        # Generate a short url
        short_id = get_new_short_url() + extension
        short_url = app.config['API_URL'] + short_id

        # Add upload in DB
        upload = Upload(file_hash_bin, short_id, file.mimetype)
        db_session.add(upload)
        db_session.commit()
    else:
        # Get old (identical) file's short_url from the hash
        og_upload = Upload.query.filter(Upload.hash == file_hash_bin).first()
        short_url =  app.config['API_URL'] + og_upload.short_url

    return jsonify(short_url=short_url)

@app.route('/<short_url>', methods=['GET'])
def get_upload(short_url):
    upload = Upload.query.filter(Upload.short_url == short_url).first()
    hash_str = str(binascii.hexlify(upload.hash).decode('utf8'))
    mimetype = upload.mime_type

    if upload.blocked:
        return redirect("http://myb.lt/#/blocked", code=420)
    else:
        return send_from_directory(app.config['UPLOAD_FOLDER'],
            hash_str, mimetype=mimetype, as_attachment=False)


@app.route('/uploads', methods=['GET'])
def get_uploads():
    err = get_auth_error()
    if err:
        return err

    uploads = Upload.query.all()
    objects = []
    for upload in uploads:
        objects.append({
        "short_url": upload.short_url,
        "blocked": upload.blocked
        })
    return jsonify(uploads=objects)


@app.route('/block/<short_url>', methods=['GET'])
def block_upload(short_url):
    err = get_auth_error()
    if err:
        return err

    upload = Upload.query.filter(Upload.short_url == short_url).first()
    upload.blocked = not upload.blocked
    db_session.commit()
    return redirect("#/admin", code=302)

@app.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    username = req['username']
    password = req['password']

    user = User.query.filter(User.username == username).first()
    if user and get_hash(password, user.salt) == user.password:
        token = uuid.uuid4().hex
        user.token = token

        db_session.query(User).filter_by(id=user.id) \
            .update({"token": user.token})
        db_session.commit()

        resp = jsonify({'success': True})
        resp.set_cookie('token', token)
        return resp

    return jsonify({'error': 'Please login'}), 401

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    init_db()
    app.run()
