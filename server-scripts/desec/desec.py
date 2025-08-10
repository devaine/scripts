#!/usr/bin/env python

import subprocess
import json
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()  # Loads up .env file

current_domain = os.getenv("CURRENT_DOMAIN")
desec_token = os.getenv("DESEC_TOKEN")
excluded_subdomains = ["mail._domainkey.mail", "mail", "_dmarc.mail"]
timeout = 1800  # In seconds, 600 = 10min, 900 = 15m, 1800 = 30min

# Credits:
# https://desec.readthedocs.io/en/latest/dns/rrsets.html#modifying-an-rrset
# for documentation


async def modifyRecords(newIP):
    args = "curl https://desec.io/api/v1/domains/" + current_domain + \
        "/rrsets/ --header 'Authorization: Token " + desec_token + "'"

    data_binary = subprocess.run(
        args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    data = data_binary.stdout.decode("utf-8")

    # convert to python object from str
    json_data = json.loads(data)

    for i in range(len(excluded_subdomains)):
        excluded_subdomains[i] = excluded_subdomains[i] + \
            "." + current_domain + "."

    for entry in json_data:
        # Only allow "A" record subdomains at the moment
        if entry["name"] not in excluded_subdomains and entry["type"] == "A":
            if (entry["records"][0] != newIP):
                subname = str(entry["subname"])  # Subdomain Name

                # Basically runs a PATCH method for the api to change
                # the ip record of all "A" record subdomains to the new
                # public ip address

                change_record_arg = \
                    "curl -X PATCH https://desec.io/api/v1/domains/" + \
                    current_domain + "/rrsets/" + subname + \
                    "/A/" + " --header 'Authorization: Token " \
                    + desec_token + "'" + " --header " + \
                    "'Content-Type: application/json' " + \
                    "--data @- <<< '{\"records\": [\"" + newIP + "\"] }'"

                # print(change_record_arg)
                subprocess.run(change_record_arg, shell=True)
                await asyncio.sleep(5)

    print("done with changing records!")


def getCurrentIP():
    print("getting current ip...")

    # Get the current Public IP to a "public_ip" file
    subprocess.run(
        ["curl", "ifconfig.me", "-o", "public_ip"], stderr=subprocess.DEVNULL)


async def newIPCheck():
    print("checking for new ips...")
    presentIPFile = open("public_ip", "r")

    newIP_curl = subprocess.run(["curl", "ifconfig.me"],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.DEVNULL)

    newIP = newIP_curl.stdout.decode("utf-8")

    if (presentIPFile.readline() == newIP):
        await asyncio.sleep(timeout)
        await newIPCheck()

    else:
        print("uh oh! public ip updated!")
        await modifyRecords(newIP)
        getCurrentIP()  # update current ip
        await newIPCheck()


def main():
    if not os.path.exists("public_ip"):
        getCurrentIP()
    elif not os.path.exists(".env"):
        print("no visible .env file for token!")
        exit(1)

    asyncio.run(newIPCheck())


if __name__ == "__main__":
    main()
