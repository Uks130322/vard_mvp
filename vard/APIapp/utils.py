import csv
import json
import requests

from vardapp.utils import get_upload_filename, get_upload_file_path


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
