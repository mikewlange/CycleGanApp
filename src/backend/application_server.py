import os, logging
from flask import Flask, flash, request, redirect, url_for, session, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
from pathlib import Path

UPLOAD_FOLDER = Path.cwd() / 'uploads/'
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
RESPONSE_FOLDER = Path.cwd() / 'response/'
Path(RESPONSE_FOLDER).mkdir(exist_ok=True)
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = b'MBWUdbxX;>]vrTL'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESPONSE_FOLDER'] = RESPONSE_FOLDER



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    app.logger.info('upload_folder = {}'.format(app.config['UPLOAD_FOLDER']))
    app.logger.info('response_folder = {}'.format(app.config['RESPONSE_FOLDER']))
    app.logger.info(request)
    app.logger.info(request.files)
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            app.logger.info('no file part')
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # TODO Lorenz: Cover case where file type is not allowed
        # TODO Lorenz: Enforce max file size limitation
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

    return render_template('index.html')

# Leaving this in for now to display how to do redirects:
# return redirect(url_for('uploaded_file',
            #                        filename=filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)