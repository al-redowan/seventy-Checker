#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requests.txt

# Run script
python credit_card_checker.py input.txt output.txt

# Deactivate virtual environment
deactivate

# t card checker script
python credit_card_checker.py "$input_file" "$output_file"
