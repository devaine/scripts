#!/usr/bin/env python

import os
from time import sleep
from dotenv import load_dotenv
import requests

load_dotenv()

# Constants
DOMAIN = os.getenv("CURRENT_DOMAIN")
DESEC_TOKEN = os.getenv("DESEC_TOKEN")
IGNORED_SUBDOMAINS_PREFIXES = ["mail._domainkey.mail", "mail", "_dmarc.mail", "skyguy"]
TIMEOUT = 10  # In seconds, 600 = 10min, 900 = 15m, 1800 = 30min

# Credits:
# https://desec.readthedocs.io/en/latest/dns/rrsets.html#modifying-an-rrset
# for documentation


def getSubDomains():
    subDomainsLink = "https://desec.io/api/v1/domains/" + DOMAIN + "/rrsets/"

    subDomainsHeader = {"Authorization": "Token " + DESEC_TOKEN}

    subDomainsRequest = requests.get(subDomainsLink, headers=subDomainsHeader)
    subDomainsJSON = subDomainsRequest.json()

    return subDomainsJSON


def filterRecords():
    filtered_prefixes = []

    getRequestIP = requests.get("https://ifconfig.me")
    requestIP = getRequestIP.text

    IGNORED_SUBDOMAINS = []
    for i in range(len(IGNORED_SUBDOMAINS_PREFIXES)):
        IGNORED_SUBDOMAINS.append(IGNORED_SUBDOMAINS_PREFIXES[i] + "." + DOMAIN + ".")

    for rrset in getSubDomains():
        IS_NOT_IGNORED = rrset["name"] not in IGNORED_SUBDOMAINS
        CONTAINS_A_RECORD = rrset["type"] == "A"
        NOT_CURRENT_IP = rrset["records"][0] != requestIP

        if IS_NOT_IGNORED and CONTAINS_A_RECORD and NOT_CURRENT_IP:
            filtered_prefixes.append(rrset["subname"])

    if len(filtered_prefixes) > 0:
        return filtered_prefixes


def changeRecords():
    prefixes = filterRecords()

    # If there are no outdated subdomains...
    if prefixes is None:
        print("No available subdomains to change")
        return

    getRequestIP = requests.get("https://ifconfig.me")
    requestIP = getRequestIP.text

    for prefix in prefixes:
        subDomainsLink = (
            "https://desec.io/api/v1/domains/" + DOMAIN + "/rrsets/" + prefix + "/A/"
        )
        subDomainsHeader = {
            "Authorization": "Token " + DESEC_TOKEN,
            "Content-Type": "application/json",
        }
        subDomainsData = {
            "subname": prefix,
            "type": "A",
            "records": [requestIP],
            "ttl": 3600,
        }

        changeSubDomainRequest = requests.put(
            subDomainsLink, json=subDomainsData, headers=subDomainsHeader
        )

        print("for prefix: " + prefix)
        print(changeSubDomainRequest.text)

        sleep(3)


def checkIP():
    if not os.path.exists("data"):
        os.mknod("data")

    dataFile = open("data", "r")

    getRequestIP = requests.get("https://ifconfig.me")
    requestIP = getRequestIP.text

    dataFileIP = dataFile.readline().replace("\n", "")

    if requestIP != dataFileIP:
        changeRecords()
        with open("data", "w") as dataFile:
            dataFile.write(requestIP)


def checkInternet():
    print("Checking Connection...")
    try:
        testRequest = requests.get("https://ifconfig.me", timeout=15)
    except (requests.Timeout, requests.ConnectionError) as exception:
        print("Connection Failed!\nReason: " + exception)
        checkInternet()

    if testRequest.text is not None:
        return True


def main():
    print("Starting Script")
    while checkInternet():
        checkIP()
        sleep(TIMEOUT)


if __name__ == "__main__":
    main()
