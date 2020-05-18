#!/bin/bash

./bf_server &
./bf_client load hashlist.txt
python app.py