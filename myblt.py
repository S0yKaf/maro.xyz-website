import os
import hashlib
import binascii
import string, random

from flask import Flask, request, send_from_directory, jsonify
from flask.ext.cors import CORS
from werkzeug import secure_filename, exceptions
from database import db_session, init_db
from models import Upload

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['BASE_URL'] = 'http://myb.lt:5000/'

cors = CORS(app, resources={r"*": {"origins": "*"}})

def contains_hash(hash):
    return Upload.query.filter(Upload.hash == hash).count() != 0

def get_new_short_url():
    # TODO check if short_id is unique
    chars = []
    for x in range(7):
        chars.append(random.choice(string.ascii_letters + string.digits))
    return ''.join(chars)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return BadRequest

    # Get sha1 of uploaded file
    m = hashlib.sha1()
    m.update(file.read())
    file_hash_bin = m.digest()

    if not contains_hash(file_hash_bin):
        # Save new file to uploads folder
        filename = secure_filename(file.filename)
        file_hash_str = str(binascii.hexlify(file_hash_bin).decode('utf8'))
        abs_file = os.path.join(app.config['UPLOAD_FOLDER'], file_hash_str)
        file.save(abs_file)

        # Generate a short url
        short_id = get_new_short_url()
        short_url = app.config['BASE_URL'] + 'upload/' + short_id

        # TODO add real mime type
        # Add upload in DB
        upload = Upload(file_hash_bin, short_id, 'mime')
        db_session.add(upload)
        db_session.commit()
    else:
        # Get old (identical) file's short_url from the hash
        # TODO give link to user of same file
        short_url =  app.config['BASE_URL'] + 'upload/' + 'TODO'
        pass

    return jsonify(short_url=short_url)

@app.route('/upload/<short_url>', methods=['GET'])
def get_upload(short_url):
    # TODO resolve short url to hash
    return send_from_directory(app.config['UPLOAD_FOLDER'], short_url)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == "__main__":
    init_db()
    app.run()
