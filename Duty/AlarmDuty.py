import requests
import json
from datetime import date, datetime, timedelta

# Objects to Parse in
class Task:
    def __init__(self, task_id, name, people_id):
        self.task_id = task_id
        self.name = name
        self.people_id = people_id

class People:
    def __init__(self, people_id, name):
        self.people_id = people_id
        self.name = name


endpoint = "https://api.float.com"
headers = {"Authorization": "Bearer 26df3bf128afcba2TolQQgadAEbqrEZ0xnxePuU9hBBgY6v7AGL0BDeEnzs"}

#++Globals
#Enter date
startdate = date(2020, 2, 26)
enddate = date(2020, 2, 27)

#Calculate numver of days
days = (enddate - startdate).days
days = days + 1
date = startdate

#-- Globals

#++get all People
request = endpoint + "/v3/people"

r = requests.get(request, headers=headers) 

people_json = (json.loads(r.text))

peoples = []

for person in people_json:
    peoples.append(People((person['people_id']), (person['name'])))

#--get all people

#Get Tasks for each day
for i in range(0,days):
    #reset all duty-counters for this day
    duty1_str = "Duty 1: "
    duty2_str = "Duty 2: "
    tier2_str = "Tier 2: "

    #get Data from Float API
    request = endpoint + "/v3/tasks?start_date=" + str(date) + "&end_date=" + str(date) 
    
    r = requests.get(request, headers=headers) 

    tasks_json = (json.loads(r.text))

    #++Json to objects
    tasks = []

    for task in tasks_json:
        tasks.append(Task((task['task_id']), (task['name']), (task['people_id'])))
        
    #--Json to objects

    #++Get duty-names
    for task in tasks:
        if(task.name == "Duty 2"):
            for person in peoples:
                if (person.people_id == task.people_id):
                    duty2_str = duty2_str + str(person.name) + " "
                    if(str(person.name == "Ramona Betschart")):
                        msg = "Du hesh am " + str(date) + " Duty 2"    
    

    #--Get Duty-name

    #Send alert to Slack, when duty is missing
    if(msg != ""):
        web_hook_url = "https://hooks.slack.com/services/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"

        slack_msg = {'text':msg}

        requests.post(web_hook_url,data=json.dumps(slack_msg))

    #Get next date
    date = date + timedelta(days=1)  
