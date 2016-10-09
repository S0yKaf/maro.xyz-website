import os
import hashlib
import binascii
import string
import random
import uuid
import sys

from flask import Flask, request, send_from_directory, jsonify, redirect
from database import db_session, init_db, init_engine

from models import Upload, User

app = Flask(__name__)


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


def get_extension(filename):
    last_dot_pos = filename.rfind('.')
    if last_dot_pos < 1:
        return None
    ext = filename[last_dot_pos + 1:]
    double_dot_pos = filename.rfind('.', 0, last_dot_pos - 1)
    if double_dot_pos == -1:
        return ext
    else:
        double_ext = filename[double_dot_pos + 1:last_dot_pos]
        if double_ext in app.config['DOUBLE_EXTS']:
            return double_ext + '.' + ext
        else:
            return ext


def extension_blocked(file):
    extension = get_extension(file.filename)
    blacklist = app.config['BLACKLIST_EXTENSIONS']

    return extension in blacklist


def new_upload(file, file_hash_bin):
    file_hash_str = str(binascii.hexlify(file_hash_bin).decode('utf8'))
    abs_file = os.path.join(app.config['UPLOAD_FOLDER'], file_hash_str)

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    file.stream.seek(0)
    file.save(abs_file)

    # Generate a short id and append extension
    short_id = get_new_short_url()
    extension = get_extension(file.filename)
    if extension:
        full_id = short_id + '.' + extension
    else:
        full_id = short_id

    # Add upload in DB
    upload = Upload(file_hash_bin, full_id, file.mimetype)
    db_session.add(upload)
    db_session.commit()

    return upload


def get_hash(password, salt):
    m = hashlib.sha512()
    m.update(salt.encode('utf8'))
    m.update(password.encode('utf8'))
    return m.digest()


def get_auth_error(semi=False):
    # If app is not configured for private usage, ignore check
    if semi and not app.config['IS_PRIVATE']:
        return

    token = request.cookies.get('token')
    if not token or not User.query.filter(User.token == token).first():
        return jsonify({'error': 'Unauthorized'}), 403


@app.route('/private', methods=['GET'])
def is_app_private():
    return jsonify({'private': app.config['IS_PRIVATE']})


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'Bad request'}), 400

    if extension_blocked(file):
        return jsonify({'error': 'File type not allowed'}), 400

    err = get_auth_error(True)
    if err:
        return err

    # Get sha1 of uploaded file
    m = hashlib.sha1()
    m.update(file.read())
    file_hash_bin = m.digest()

    if hash_exists(file_hash_bin):
        # Get old (identical) file's short_url from the hash
        upload = Upload.query.filter(Upload.hash == file_hash_bin).first()
    else:
        upload = new_upload(file, file_hash_bin)

    if not upload:
        return jsonify({'error': 'An unknown error occurred'}), 500

    return jsonify(short_url=app.config['API_URL'] + upload.short_url)


@app.route('/<short_url>', methods=['GET'])
def get_upload(short_url):
    upload = Upload.query.filter(Upload.short_url == short_url).first()

    if not upload:
        return '404 not found'

    hash_str = str(binascii.hexlify(upload.hash).decode('utf8'))
    mimetype = upload.mime_type

    if upload.blocked:
        return redirect("/#/blocked", code=301)
    else:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
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
            "blocked": upload.blocked,
            "mime_type": upload.mime_type,
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
    return jsonify({'success': True}), 200


@app.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    if 'username' not in req or 'password' not in req:
        return jsonify({'error': 'Bad request'}), 400
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

    return jsonify({'error': 'Bad login'}), 401


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    app.config.from_pyfile('config/default_config.py')

    if len(sys.argv) == 2:
        conf = sys.argv[1]
        print('Loading additional config %s...', conf)
        app.config.from_pyfile('config/' + conf + '_config.py')

    init_engine(app.config['DATABASE_URI'])
    init_db()
    app.run()
