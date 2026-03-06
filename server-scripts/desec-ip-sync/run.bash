#!/bin/bash

if [ ! -f .env ]; then
	env | grep DESEC_TOKEN >>.env
	env | grep CURRENT_DOMAIN >>.env
fi

# If virtual environment does exist..
if [ ! -d venv ]; then
	python3 -m venv venv
	source venv/bin/activate
	pip install -U python-dotenv requests
	pip install -U pip # Update pip to the latest version
else
	source venv/bin/activate
fi
