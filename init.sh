#!/bin/bash

./bf_server &
./bf_client load hash.db
python app.py