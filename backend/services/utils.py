import os
import time

from werkzeug.utils import secure_filename
from datetime import datetime
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
        os.makedirs(app.config['FILE_UPLOAD_DIR'], exist_ok=True)
        file.save(file_path)  # save the picture
        return timestamped_filename


def validate_form_data(data):
    def get_trimmed(value):
        return value.strip() if isinstance(value, str) else ''

    today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

    # Optional fields: if present and not all spaces
    for key, value in data.items():
        if isinstance(value, str) and get_trimmed(value) == '':
            return {'success': False, 'error': f'{key.replace("_", " ").capitalize()} cannot be empty or only contain Spaces.'}

    # Password match check
    if 'password' in data and 'confirm_password' in data:
        if data['password'] != data['confirm_password']:
            return {'success': False, 'error': 'Passwords do not match!'}

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d')
        except (ValueError, TypeError):
            return None

    # Parse and check dates only if keys exist
    birth_date = parse_date(data.get('birth_date')) if 'birth_date' in data else None
    death_date = parse_date(data.get('death_date')) if 'death_date' in data else None
    photo_date = parse_date(data.get('photo_date')) if 'photo_date' in data else None

    if birth_date and birth_date > today:
        return {'success': False, 'error': "Birth date cannot be in the future. What do you think you're doing?!"}
    if death_date and death_date > today:
        return {'success': False, 'error': "Death date cannot be in the future. What do you think you're doing?!"}
    if photo_date and photo_date > today:
        return {'success': False, 'error': "Timeline date cannot be in the future. What do you think you're doing?!"}
    if birth_date and death_date and birth_date > death_date:
        return {'success': False, 'error': 'Birth date must be before death date!'}

    return {'success': True, 'error': ''}

