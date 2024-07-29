"""Script with functions to get paths and names for uploading files"""

from datetime import datetime as dt
import os
import csv
import json
import requests


def load_json(self, validated_data):
    response = requests.get(validated_data['load_by_url'])
    datas = response.json()
    filename = get_upload_filename(validated_data['user_id'], 'json')
    link = get_upload_file_path(validated_data['user_id'], filename)
    outfile = open(link, "w")
    json.dump(datas, outfile)
    outfile.close()
    validated_data['link'] = link
    if not validated_data['name']:
        validated_data['name'] = filename
    return validated_data


def load_csv(self, validated_data):
    response = requests.get(validated_data['load_by_url'])
    datas = csv.reader(response.text)
    filename = get_upload_filename(validated_data['user_id'], 'csv')
    link = get_upload_file_path(validated_data['user_id'], filename)
    outfile = open(link, "w")
    writer = csv.writer(outfile)
    writer.writerow(datas)
    outfile.close()
    validated_data['link'] = link
    if not validated_data['name']:
        validated_data['name'] = filename
    return validated_data


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
