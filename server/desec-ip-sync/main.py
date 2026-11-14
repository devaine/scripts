#!/usr/bin/env python

# TODO: Figure out a way to update the text file using a bash script that the program can read whilst running
# for the IGNORED_SUBDOMAINS_PREFIXES variable

import os
import sys
import argparse
from time import sleep
from dotenv import load_dotenv
import requests
import json
from collections import Counter

load_dotenv()

# Constants
DOMAIN = os.getenv("CURRENT_DOMAIN")
DESEC_TOKEN = os.getenv("DESEC_TOKEN")
#IGNORED_SUBDOMAINS_PREFIXES = ["mail._domainkey.mail", "mail", "_dmarc.mail", "skyguy"]
TIMEOUT = 1800  # In seconds, 600 = 10min, 900 = 15m, 1800 = 30min
DESEC_TIMEOUT = 5  # Timeout for the API Queries

# Credits:
# https://desec.readthedocs.io/en/latest/dns/rrsets.html#modifying-an-rrset
# for documentation


def getSubDomains():
    subDomainsLink = "https://desec.io/api/v1/domains/" + DOMAIN + "/rrsets/"

    subDomainsHeader = {"Authorization": "Token " + DESEC_TOKEN}

    subDomainsRequest = requests.get(subDomainsLink, headers=subDomainsHeader)

    return subDomainsRequest


def getCurrentIP():
    rrsetList = getSubDomains().json()

    rrsetList_json = json.loads(rrsetList)

    for rrset in rrsetList_json:
        print(type(rrset), repr(rrset))

    #rrsetList.append(rrset[0])

    #value, count = Counter(rrsetList).most_common(1)[0]

    return None


def filterRecords():
    ignoredSubdomains = []
    filteredSubdomains = []
    ISEMPTY = False

    if not os.path.isfile("./data/ignoredSubdomains"):
        open(os.path.join("./data/", "ignoredSubdomains"), "w").close()
        ISEMPTY = True

    if not ISEMPTY:
        with open(os.path.join("./data/", "ignoredSubdomains"), "r") as ignoredSubdomainsFile:
            for subdomain in ignoredSubdomainsFile:
                ignoredSubdomains.append(subdomain)

    for rrset in getSubDomains():
        IS_NOT_IGNORED = rrset["name"] not in ignoredSubdomains
        CONTAINS_A_RECORD = rrset["type"] == "A"
        NOT_CURRENT_IP = rrset["records"][0] != requestIP

        if IS_NOT_IGNORED and CONTAINS_A_RECORD and NOT_CURRENT_IP:
            filteredSubdomains.append(rrset["subname"])

    if len(filteredSubdomains) > 0:
        return filteredSubdomains
    else:
        return None


def changeRecords():
    subdomains = filterRecords()

    # If there are no outdated subdomains...
    if subdomains is None:
        print("No available subdomains to change")
        return

    for subdomain in subdomains:
        subDomainsLink = (
            "https://desec.io/api/v1/domains/" + DOMAIN + "/rrsets/" + subdomain + "/A/"
        )
        subDomainsHeader = {
            "Authorization": "Token " + DESEC_TOKEN,
            "Content-Type": "application/json",
        }
        subDomainsData = {
            "subname": subdomain,
            "type": "A",
            "records": [requestIP],
            "ttl": 3600,
        }

        changeSubDomainRequest = requests.put(
            subDomainsLink, json=subDomainsData, headers=subDomainsHeader
        )

        print("DEBUG: For subdomain: " + subdomains)
        print(changeSubDomainRequest.text)

        sleep(DESEC_TIMEOUT)


def checkIP():
    # Grab the current IP from the desec API
    if not os.path.isfile("./data/currentIP"):
        with open(os.path.join("./data/", "currentIP"), "w") as currentIPFile:
            currentIPFile.write(getCurrentIP())
            currentIPFile.close()

    # Request IP from website
    global requestIP
    getRequestIP = requests.get("https://ifconfig.me")
    requestIP = getRequestIP.text

    # Grab file data and close for data safety.
    currentIPFile = open(os.path.join("./data/", "currentIP"), "r")
    currentIP = currentIPFile.readline().replace("\n", "")
    currentIPFile.close()

    # If both IP's are differnet (New external IP!)
    if requestIP != currentIP:
        changeRecords()
        with open(os.path.join("./data/", "currentIP"), "w") as currentIPFile:
            currentIPFile.write(requestIP)
            currentIPFile.close()
        print("All IP's Changed!")
    else:
        print("DEBUG: No new IP found!")
        print(f"DEBUG: New IP={requestIP}")
        print(f"DEBUG: Current IP={currentIP}")


# NOTE: This function will always run even without internet available.
def checkInternet():
    print("DEBUG: Checking Connection...")
    try:
        testRequest = requests.get("https://ifconfig.me", timeout=15)
    except (requests.Timeout, requests.ConnectionError) as exception:
        if (exception):
            print("DEBUG: Connection failed!")
            checkInternet()

    if testRequest.text is not None:
        return True


def appendSubdomain(args: list):
    with open(os.path.join("./data/", "ignoredSubdomains"), "a") as ignoredSubdomainsFile:
        for subdomain in args:
            ignoredSubdomainsFile.write(subdomain + "\n")
            print("Added subdomain: " + subdomain)


def main():
    parser = argparse.ArgumentParser(prog="main.py")
    parser.add_argument("-a", "--append", nargs="+")
    if parser.parse_args().append is not None:
        appendSubdomain(parser.parse_args().append)
        sys.exit(1)

    print("Starting Script")
    while checkInternet():
        checkIP()
        sleep(TIMEOUT)


if __name__ == "__main__":
    main()
