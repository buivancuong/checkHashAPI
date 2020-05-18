from flask import Flask
from flask import request
from flask import jsonify
import os
import subprocess
import re


app = Flask(__name__)


@app.route('/')
def index():
    return 'Flask is running!'


@app.route('/data')
def names():
    data = {"names": ["John", "Jacob", "Julie", "Jennifer"]}
    return jsonify(data)

@app.route('/api/v1/check_hash')
# GET /api/v1/check_hash?hash=blahblahblah
def check_hash():
    hash_value = request.args.get('hash')
    check_command = './bf_client check ' + str(hash_value)

    result_command = subprocess.check_output(check_command, shell=True)

    nonexistant = re.search('no.*', str(result_command))

    if nonexistant: return jsonify("nonexistant")
    else: return jsonify("exist")


#if __name__ == '__main__':
#    app.run()
if __name__ == '__main__':
     app.run(host='127.0.0.1', port=5050, debug=True, ssl_context=('server.crt', 'server.key'))