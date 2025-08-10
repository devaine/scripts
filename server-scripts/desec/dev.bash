#!/bin/bash

# If virtual environment does exist..
if [ ! -d .venv ]; then
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -U python-dotenv
	pip install --upgrade pip # Update pip to the latest version
fi

echo 'Make sure to run ". .venv/bin/activate" to enter the development environment'
