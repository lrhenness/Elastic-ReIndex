#!/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import http

http.client.HTTPConnection.debuglevel = 1

username = 'elastic'
password = 'Hunter1'
host = 'localhost'
port = '9200'

def delete_index(source):
    print("The program has indicated that the reindex of " + source + " is now complete and the index should be deleted")
    #Comment the following to prevent deleting indices during testing
    """ try:
        curl -X DELETE "https://" host + ":" + port + "/" + source
    except:
        print("An error occured with deletion of " + source + " - Task ID: " + task)
        exit() #exit program """

def check_task(task, source): #Check on the task:
    status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json() #GET task information
    while status["completed"] != "true": #Task not complete, print status message and wait
        progress = (int(status["task"]["status"]["created"]) / int(status["task"]["status"]["total"])) * 100
        print("waiting for task" + task + "to complete. Progress: " + progress + "%")
        time.sleep(5)
        status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
    delete_index(source)

def reindex(list):
    header = "https://" + host + ":" + port + "/_reindex?wait_for_completion=false" #build authenticated request URL passing creds:
    for line in list:
        split = line.split(":") #Split the current line in the text file by semicolon
        print("Reindexing: " + split[0] + " => " + split[1])
        #Build POST:
        body = "{\"source\":{\"index\":" + split[0] + "},\"dest\":{\"index\":" + split[1] + "}}"
        #Send POST and gather .task returned by combining post & body
        try:
            resp = requests.post(header, data=body, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
        except:
            print("An error occured while sending the reindex POST with the following request:")
            print("header: " + header)
            print("body:   " + body)
            print("Please see the Python error for more details.")
            exit()
        #Check if complete before continuing
        check_task(resp["task"], split[0])

def main():
    list = open("list.txt", "r") #Gather The list of indices to reindex from semi-colon KV pair line-delimited text file (is there a better way?)
    #Example of text file (no quotes):
    """
    logstash-dev-serilog-2021.02.19:logstash-dev-serilog-reindex
    logstash-dev-serilog-2021.02.20:logstash-dev-serilog-reindex
    logstash-dev-serilog-2021.02.21:logstash-dev-serilog-reindex
    logstash-qa-serilog-2021.02.19:logstash-qa-serilog-reindex
    logstash-qa-serilog-2021.02.20:logstash-qa-serilog-reindex
    """
    print("")
    print(list)
    if input("Would you like to reindex all of the above? [y/n]") == "y":
        print("Reindexing...")
        reindex(list)
        exit()
    else:
        print("Exiting...")
        exit()

main()