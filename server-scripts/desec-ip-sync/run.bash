#!/bin/bash

# If virtual environment does exist..
if [ ! -d venv ]; then
	python3 -m venv venv
	source venv/bin/activate
	pip install -U python-dotenv requests
	pip install -U pip # Update pip to the latest version
else
	source venv/bin/activate
fi

python main.py
