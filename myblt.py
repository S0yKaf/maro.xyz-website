import os
from flask import Flask, request, send_from_directory, jsonify
from flask.ext.cors import CORS
from werkzeug import secure_filename

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
app.config['BASE_URL'] = 'http://localhost:5000/'

cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file: # TODO add check if sha1 already exists
        filename = secure_filename(file.filename)
        file_hash = filename
        abs_file = os.path.join(app.config['UPLOAD_FOLDER'], file_hash)
        file.save(abs_file)

        # TODO-actually generate a short url
        short_id = file_hash
        # TODO register upload in db
        short_url = app.config['BASE_URL'] + 'upload/' + short_id
    return jsonify(uploaded_file=filename, short_url=short_url)

@app.route('/upload/<filename>', methods=['GET'])
def get_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run()
