#!/usr/bin/env bash

echo "clean up venv"
rm -r venv

echo "create virtual venv"
python3 -m venv venv

echo "activate virtual venv"
. venv/bin/activate

echo "install requirements"
pip install -r requirements.txt

echo "set app.py executable permission"
chmod +x app.py

echo "deactivate venv"
deactivate

echo "installation complete"
