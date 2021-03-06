from itertools import repeat
from flask import Flask, request, url_for
import json
from random import randint
import uuid

app = Flask(__name__)

pids = dict()


def extract_prefix(pid):
    return pid.split('/', 1)[0] + '/'


def extract_suffix(pid):
    return pid.split('/', 1)[1]


def get_prefixes(pids_dictionary):
    return list(set(map(extract_prefix, pids_dictionary)))


def get_suffixes(pids, prefix):
    return {extract_suffix(k) for k, v in list(pids.items()) if k.startswith(prefix)}


@app.route('/', methods=['GET'])
def get_prefix_list():
    # dengerous but epic does it like that
    return json.dumps(get_prefixes(pids))


@app.route('/<prefix>/', methods=['GET'])
def get_pids(prefix):
    return json.dumps(list(get_suffixes(pids_dictionary=pids, prefix=prefix)))


@app.route('/<prefix>/<suffix>', methods=['GET'])
def get_pid(prefix, suffix):
    pid = '%s/%s' % (prefix, suffix)
    if pid in pids:
        #it should be json already
        return pids[pid]

    return 'Not found', 404


@app.route('/<prefix>/<suffix>', methods=['PUT'])
def add_pid(prefix, suffix):
    app.logger.debug('Uploaded data: %s\n' % request.data)
    pids[('%s/%s' % (prefix, suffix))] = request.data
    return ('You updated pid %s // %s' % (prefix, suffix)), 201, {
        'Location': url_for('get_pid', prefix=prefix, suffix=suffix)}


@app.route('/<prefix>/<suffix>', methods=['DELETE'])
def delete_pid(prefix, suffix):
    app.logger.debug('Delete pid: %s/%s\n' % (prefix, suffix))
    deleted_pid = pids.pop(('%s/%s' % (prefix, suffix)), False)
    if not deleted_pid:
        return 'Not found', 404
    else:
        return ('You deleted pid %s/%s' % (prefix, suffix)), 204


def generate_suffix():
    return str(uuid.uuid1())


@app.route('/<prefix>/', methods=['POST'])
def create_pid(prefix):
    condition = True
    while condition:
        suffix = generate_suffix()
        pid = '%s/%s' % (prefix, suffix)
        condition = pid in pids

    pids[pid] = request.data
    return ('You updated pid %s\nValue:%s\n' % (pid, request.data)), 201, {
        'Location': url_for('get_pid', prefix=prefix, suffix=suffix)}


def convert_to_handle(location, checksum):
    if checksum:
        new_handle_json = json.dumps([{'type': 'URL',
                                       'parsed_data': location},
                                      {'type': 'CHECKSUM',
                                       'parsed_data': str(checksum)}])
    else:
        new_handle_json = json.dumps([{'type': 'URL',
                                       'parsed_data': location}])
    return new_handle_json


@app.before_first_request
def populate_pids():
    prefixes = ['8441', '90210', '44']
    location_string = 'irods://zone:1247/home/eudat/'
    for prefix in prefixes:
        for _ in repeat(None, randint(5, 10)):
            suffix = generate_suffix()
            location = '%s/%s' % (location_string, suffix)
            checksum = str(uuid.uuid1())
            pids['%s/%s' % (prefix, suffix)] = convert_to_handle(
                location=location, checksum=checksum)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
