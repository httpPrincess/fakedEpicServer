import flask
from flask import Flask
from flask import request
from flask import url_for

import json

app = Flask(__name__)

pids = dict()


def extract_prefix(pid):
    return pid.split('/', 1)[0] + '/'


def extract_suffix(pid):
    return pid.split('/', 1)[1]


def get_prefixes(pids):
    return map(extract_prefix, pids)


def get_suffixes(pids, prefix):
    return {extract_suffix(k) for k, v in pids.iteritems() if k.startswith(prefix)}


#{k: v for k,v in pids.iteritems() if k.count('8444/')}

@app.route('/', methods=['GET'])
def get_prefix_list():
    #dengerous but epic does it like that
    return json.dumps(get_prefixes(pids))


@app.route('/<prefix>/', methods=['GET'])
def get_pids(prefix):
    return json.dumps(list(get_suffixes(pids=pids, prefix=prefix)))


@app.route('/<prefix>/<suffix>', methods=['GET'])
def get_pid(prefix, suffix):
    pid = '%s/%s' % (prefix, suffix)
    if pids.has_key(pid):
        #it should be json already
        return pids[pid]

    return 'Not found', 404


@app.route('/<prefix>/<suffix>', methods=['PUT'])
def add_pid(prefix, suffix):
    pids[('%s/%s' % (prefix, suffix))] = request.data
    return ('You updated pid %s // %s' % (prefix, suffix)), 201, {
        'Location': url_for('get_pid', prefix=prefix, suffix=suffix)}


@app.before_first_request
def populate_pids():
    pids['8444/21211'] = "{'key':'value', 'key2':'value2'}"
    pids['85411/dasa'] = "{'ada':'daa', 'foo':'bar'}"
    pids['85444/foobar'] = "{'key1':'value1', 'key2':'value2'}"


if __name__ == '__main__':
    app.run(debug=True)
