from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import os
import subprocess
import re
import json

import logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

key_list = list()

with open('keys.txt') as keys_file:
    key = keys_file.readline()
    while key:
        key = key.rstrip('\n')
        key_list.append(key)
        key = keys_file.readline()

app = Flask(__name__)


@app.route('/api/v1/check_hash')
# GET /api/v1/check_hash?hash=blahblahblah&apikey=blahblahblah
def check_hash():

    api_key_value = request.args.get('apikey')

    exist_key = False
    for key in key_list:
        if api_key_value == key:
            exist_key = True
            break
    
    if not exist_key:
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response

    hash_value = request.args.get('hash')
    check_command = './bf_client check ' + str(hash_value)

    result_command = subprocess.check_output(check_command, shell=True)

    nonexistant = re.search('no.*', str(result_command))

    if nonexistant: return jsonify({"Message": "nonexistant"})
    else: return jsonify({"Malware": str(result_command)})


#if __name__ == '__main__':
#    app.run()
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5050, debug=True, ssl_context=('server.crt', 'server.key'))