#!/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import http

debug = True
username = 'admin'
password = 'hunter1'
host = 'localhost'
port = '9200'

def delete_index(source):
    print("The program has indicated that the reindex of " + source + " is now complete and the index should be deleted")
    if input("Would you like to delete the source? [y/n]") == "y":
        print("Deleting...")
        time.sleep(1)
        try:
            resp = requests.delete("https://" + host + ":" + port + "/" + source, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
            if debug:
                print("====response====")
                print(resp)
        except:
            print("An error occured with deletion of " + source)
            exit() #exit program
    else:
        print("Source not deleted, moving on...")
        time.sleep(1)

def check_task(task, source): #Check on the task:
    status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json() #GET task information
    while str(status["completed"]) != "true": #Task not complete, print status message and wait
        p_created = status["task"]["status"]["created"]
        p_total = status["task"]["status"]["total"]
        progress = ( int(p_created) / int(p_total) ) * 100
        print("waiting for task " + task + " to complete. " + str(p_created) + " out of " + str(p_total) + " docs reindexed. Progress: " + str(progress) + "%")
        time.sleep(5)
        status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
        if debug:
            print("API response for task completed: " + str(status["completed"]))
    delete_index(source)

def reindex(list):
    header = "https://" + host + ":" + port + "/_reindex?wait_for_completion=false" #build authenticated request URL passing creds:
    for line in list:
        split = line.split(":") #Split the current line in the text file by semicolon
        source = split[0]
        destination = split[1].strip()
        print("Reindexing: " + source + " => " + destination)
        #Build POST:
        body = '{"source":{"index":"' + source + '"},"dest":{"index":"' + destination + '"}}'
        body = json.loads(body)
        #Send POST and gather .task returned by combining post & body
        try:
            resp = requests.post(header, json=body, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
        except:
            print("An error occured while sending the reindex POST. Please check the configured host, port, and/or credentials.")
            exit()
        #Check if complete before continuing
        if debug:
            print("=====header=====")
            print(header)
            print("======body======")
            print(body)
            print("====response====")
            print(resp)
        check_task(resp["task"], source)

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

if debug:
    http.client.HTTPConnection.debuglevel = 1
main()