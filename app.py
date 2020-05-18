from flask import Flask
from flask import request
from flask import jsonify
import os
import subprocess
import re

import logging
logging.basicConfig(filename='app.log', filemode='w', level=logging.WARNING,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


app = Flask(__name__)


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
     app.run(host='0.0.0.0', port=5050, debug=True, ssl_context=('server.crt', 'server.key'))