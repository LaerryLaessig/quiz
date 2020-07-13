#!/usr/bin/env bash

echo "activate virtual venv"
. venv/bin/activate

echo "set admin user and pw"
export USER_ADMIN='admin'
export PWD_ADMIN='admin'
export SECRET_KEY='secret_key'

echo "start server"
python app.py

echo "deactivate venv"
deactivate
