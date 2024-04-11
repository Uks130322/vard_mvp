"""Script with functions to get paths and names for uploading files"""

from datetime import datetime as dt
import os


def user_directory_path(instance, filename):
    """Function to get path for File.link"""
    return os.path.join(f'user_{instance.user_id.id}', filename)


def get_upload_file_path(user_id, filename):
    path = os.path.join('files', f'user_{user_id.id}')
    if not os.path.isdir(path):
        os.mkdir(path)
    return os.path.join(path, filename)


def get_upload_filename(user_id, file_type):
    return f"{str(dt.timestamp(dt.now())).replace('.', '')}.{file_type}"
