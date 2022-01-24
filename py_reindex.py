#!/usr/bin/env python
import requests
from requests.auth import HTTPBasicAuth
import json
import time
import http
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

debug = False
disable_delete_confirmation = True
username = 'admin'
password = 'hunter2'
host = 'localhost'
port = '9200'

def delete_index(source):
    resp = requests.delete("https://" + host + ":" + port + "/" + source, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
    return resp

def check_task(task, list_current, list_total): #Check on the task:
    status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json() #GET task information
    while str(status["completed"]) != "True": #Task not complete, print status message and wait
        p_created = status["task"]["status"]["created"]
        p_total = status["task"]["status"]["total"]
        try:
            progress = ( int(p_created) / int(p_total) ) * 100
            progress = "{:.2f}".format(progress)
        except:
            if debug:
                print("Divide by zero error. Values:")
                print("Created: " + str(p_created))
                print("Total: " + str(p_total))
            progress = 0
        print("Waiting for task " + task + " to complete. " + str(p_created) + " out of " + str(p_total) + " docs reindexed. Task progress: " + str(progress) + "%")
        list_percentage = ( int(list_current) / int(list_total) ) * 100
        list_percentage = "{:.2f}".format(list_percentage)
        print("Total list progress: " + str(list_current) + " out of " + str(list_total) + " indices reindexed. Percentage: " + str(list_percentage) + "%")
        time.sleep(5)
        status = requests.get("https://" + host + ":" + port + "/_tasks/" + task, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
        if debug:
            print("API response for task completed: " + str(status["completed"]))
    #Add checks here for errors in the task status response.
    if int(status["task"]["status"]["created"]) == int(status["task"]["status"]["total"]):
        return True #Reindex complete, return completed = True
    else:
        return False #There was probably an error, return completed = False

def reindex(body):
    header = "https://" + host + ":" + port + "/_reindex?wait_for_completion=false" #build authenticated request URL passing creds:
    try:
        resp = requests.post(header, json=body, timeout=10, verify=False, auth=HTTPBasicAuth(username, password)).json()
    except:
        print("An error occured while sending the reindex POST. Please check the configured host, port, and/or credentials.")
        exit()
    if debug:
        print("=====header=====")
        print(header)
        print("======body======")
        print(body)
        print("====response====")
        print(resp)
    return resp

def main():
    errors = [] #Initialize error list
    with open("list.txt", "r") as file:
        print("Lines in file:")
        file_length = 0
        for line in file:
            file_length = file_length + 1
            print(line.strip())
        if input("Would you like to reindex all of the above? [y/n]") == "y":
            print("Reindexing...")
            file.close()
        else:
            print("Exiting...")
            exit()
        i = 0 #Current index of list for updating progress status in check_task() function
    with open("list.txt", "r") as file:
        for line in file:
            split = line.split(":") #Split the current line in the text file by semicolon
            source = split[0]
            destination = split[1].strip()
            print("Reindexing: " + source + " => " + destination)
            #Build POST:
            body = '{"source":{"index":"' + source + '"},"dest":{"index":"' + destination + '"}}'
            body = json.loads(body)
            resp = reindex(body) #Send Reindex POST
            complete = check_task(resp["task"], i, file_length) #Pass task ID, current list index, and total list length
            if complete:
                if disable_delete_confirmation:
                    print("Reindex of " + source + " is now complete. Deleting the the source index and moving on!")
                    resp = delete_index(source)
                    if debug:
                        print("====response====")
                        print(resp)
                else:
                    print("The program has indicated that the reindex of " + source + " is now complete and the index should be deleted")
                    if input("Would you like to delete the source? [y/n]") == "y":
                        print("Deleting...")
                        time.sleep(1)
                        resp = delete_index(source)
                        if debug:
                            print("====response====")
                            print(resp)
                    else:
                        print("Source not deleted, moving on...")
                        time.sleep(1)
            else:
                print("There was an error when reindexing the source: " + source + " - Adding to error queue and moving on. Task: " + resp["task"])
                errors.append(str(resp["task"]))
            i = i + 1
    if len(errors) == 0:
        print("All reindex tasks completed without error! Exiting.")
        exit()
    else:
        print("There were errors detected with the following tasks. This may be an index template issue.")
        print(*errors, sep = "\n")
        print("Use the following to check the tasks in Kibana Dev Tools:     GET /_tasks/TASK_ID")
        exit()

if debug:
    http.client.HTTPConnection.debuglevel = 1
main()