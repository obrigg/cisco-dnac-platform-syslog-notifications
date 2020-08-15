# =========================================================================== #
#                                                                             #
#  Cisco DNA Center Webhook-to-syslog                ||         ||            #
#                                                    ||         ||            #
#  Script: run.py                                   ||||       ||||           #
#                                               ..:||||||:...:||||||:..       #
#  Author: Robert Csapo & Oren Brigg           ------------------------       #
#                                              C i s c o  S y s t e m s       #
#  Version: 0.9 beta                                                          #
#                                                                             #
# =========================================================================== #

import json
import os
from flask import Flask, request
import logging.handlers
import argparse

def sendData (data, args):
    if args.verbose:
        print()
        print(data)
        print()

    issueTitle = (data["details"]["Type"] + " " +data["details"]["Device"])
    issuePriority = data["details"]["Assurance Issue Priority"]
    issueSeverity = data["severity"]
    issueSummary = data["details"]["Assurance Issue Details"]

    data = "Warning Severity %s (%s)! %s - %s" % (issueSeverity, issuePriority, issueTitle, issueSummary)

    dnac_logger.info(str(data))
    return("Cisco DNA Center JSON Payload received")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def mainPage():
    if request.method == 'GET':
        if args.verbose:
            print("returning: cisco-dnac-platform-syslog-notifications -> by Robert Csapo (robert@nigma.org) and Oren Brigg (Oren.Brigg@gmail.com)")
        return("cisco-dnac-platform-syslog-notifications -> by Robert Csapo (robert@nigma.org) and Oren Brigg (Oren.Brigg@gmail.com)")
    elif request.method == 'POST':
        return("cisco dna center healthcheck")

@app.route('/dnac', methods=['POST'])
def dnacPayload():
    data = request.json
    if not len(data) == 0:
        return(sendData (data, args))
    else:
        return("Connection Alive")

@app.route('/sample', methods=['GET'])
def sample():
    jsonFile = "outputdata.json"
    with open(jsonFile) as f:
        data = json.load(f)

    sendData (data, args)
    return("Sample data from -> %s" % jsonFile)

@app.route('/postsample', methods=['POST'])
def postSample():
    data = request.json

    sendData (data, args)
    return("Sample JSON Payload received")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='cisco-dnac-platform-syslog-notifications version 1.3.1')
    parser.add_argument('--ssl', action='store_true', help="please enable SSL TODO")
    parser.add_argument('--verbose', action='store_true', help="Vernose mode")
    parser.add_argument('--syslog', help="please enter the IP address of the syslog server")
    parser.add_argument('--port', help="please enter the UDP of the syslog server, default port is 514", type=int, default=514)
    args = parser.parse_args()

    # Creating the logger
    dnac_logger = logging.getLogger('dnac_logger')
    dnac_logger.setLevel(logging.INFO)

    if args.syslog is None:
        raise Exception("Sorry, no syslog server is set")

    #Creating the logging handler, directing to the syslog server
    handler = logging.handlers.SysLogHandler(address = (args.syslog,args.port))
    dnac_logger.addHandler(handler)

    print("\n ************************************************* \n")
    if args.verbose:
        print(" * Verbose Enabled")
    else:
        print(" * Verbose Disabled")

    if args.ssl is True:
        print(" * SSL Enabled (ADHOC)")
        app.run(host="0.0.0.0", port=5000, threaded=True, debug=False, ssl_context='adhoc')
    else:
        app.run(host="0.0.0.0",port=5000,threaded=True,debug=False)
