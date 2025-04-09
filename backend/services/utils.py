import os
import time

from werkzeug.utils import secure_filename

from backend import app


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def picUpdate(request):
    file = request.files['pic']
    filename=None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        name, ext = os.path.splitext(filename)
        # Add a timestamp to the file name
        timestamped_filename = f"{name}_{int(time.time())}{ext}"

        file_path = os.path.join(app.config['FILE_UPLOAD_DIR'], timestamped_filename)
        file.save(file_path)  # save the picture
    return filename