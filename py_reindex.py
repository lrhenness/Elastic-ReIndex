#!/usr/bin/env python
import requests
import json
import time

usernme = #Gather credentials from client_info.json
password = #Gather credentials from client_info.json
host = #Gather host from ?
port = 9200
list = open("list.txt", "r") #Gather The list of indices to reindex from semi-colon KV pair line-delimited text file (is there a better way?)
    #Example of text file:
    """
    logstash-dev-serilog-2021.02.19:logstash-dev-serilog-reindex
    logstash-dev-serilog-2021.02.20:logstash-dev-serilog-reindex
    logstash-dev-serilog-2021.02.21:logstash-dev-serilog-reindex
    logstash-qa-serilog-2021.02.19:logstash-qa-serilog-reindex
    logstash-qa-serilog-2021.02.20:logstash-qa-serilog-reindex
    """

def check_task(task): #Check on the task:
    get = json.loads(requests.get("https://" + host + ":" + port + "/_tasks/" + task)) #GET task information and convert JSON response to Python dictionary
    while get["completed"] != "true": #Task not complete, print status message and wait
        print("waiting for task" + task + "to complete. Progress: " + (((get["task"]["status"]["created"]/get["task"]["status"]["total"])*100)) + "%")
        time.sleep(5)
        get = json.loads(requests.get("https://" + host + ":9200/_tasks/" + task))
    try:
        curl -X DELETE "https://" host + ":" + port + "/" + split[0]
    except:
        print("An error occured with deletion of " + split[0] + " - Task ID: " + task)
        exit() #exit program

#build authenticated request URL passing creds:
post = requests.post("https://" + host + ":" + port + "/_reindex?wait_for_completion=false")

for line in list:
    split = line.split(":") #Split the current line in the text file by semicolon
    #Build POST:
    body = "{\"source\":{\"index\":" + split[0] + "},\"dest\":{\"index\":" + split[1] + "}}"
    #Send POST and gather .task returned by combining post & body
    resp = json.loads(SEND_REQUEST_HERE)
    #Check if complete before continuing
    task = resp["task"]
    check_task(task)
