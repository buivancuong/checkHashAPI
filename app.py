from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import os
import subprocess
import re
import json
import math
from hmac import compare_digest

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
    if api_key_value is None:
        logging.warning("Lack input value \"apikey\"")
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response

    exist_key = False
    for key in key_list:
        if compare_digest(api_key_value, key):      # avoid Timing attack
            exist_key = True
            break
    
    if not exist_key:
        logging.warning("Received a fail apikey")
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response

    hash_value = request.args.get('hash')
    if hash_value is None:
        logging.warning("Lack input value \"hash\"")
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response

    # Check vulnerability of input hash_value
    # First: hash length is exponetial of 2
    if math.log2(len(hash_value)) != int(math.log2(len(hash_value))):
        logging.warning("Fail input value \"hash\"")
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response
    
    # Second: hash length is too long
    if (len(hash_value) > 256):
        logging.warning("Too long input value \"hash\"")
        response = Response(json.dumps({"Message": "404 NOT FOUND"}))
        response.status_code = 404
        return response
    
    # Third: check each character for hexa decimal character
    for char in hash_value:
        try:
            int('0x' + char, 16)
        except ValueError as err:
            logging.error("Invalid character in hash input: " + err)
            response = Response(json.dumps({"Message": "404 NOT FOUND"}))
            response.status_code = 404
            return response

    check_command = './bf_client check ' + str(hash_value)
    result_command = subprocess.check_output(check_command, shell=True)

    nonexistant = re.search('no.*', str(result_command))
    if nonexistant: return jsonify({"Message": "nonexistant"})
    else: return jsonify({"Malware": str(result_command)})


#if __name__ == '__main__':
#    app.run()
if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5050, debug=True, ssl_context=('server.crt', 'server.key'))