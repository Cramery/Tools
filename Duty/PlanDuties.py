import requests
import json
from datetime import date, datetime, timedelta

# Objects to Parse in
class Task:
    def __init__(self, task_id, name, people_id, project_id):
        self.task_id = task_id
        self.name = name
        self.people_id = people_id
        self.project_id = project_id


endpoint = "https://api.float.com"
headers = {"Authorization": "Bearer "}

#++Globals
#Enter date
startdate = date(2020, 3, 5)
enddate = date(2020, 3, 5)

#Calculate numver of days
days = (enddate - startdate).days
days = days + 1
date = startdate

duty1_str = "Duty 1: "
duty2_str = "Duty 2: "
tier2_str = "Tier 2: "

#-- Globals

#++get all People
request = endpoint + "/v3/people"

r = requests.get(request, headers=headers) 

people_json = (json.loads(r.text))

people = []

for person in people_json:
    people.append(person['people_id'])

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
        tasks.append(Task((task['task_id']), (task['name']), (task['people_id']), (task['project_id'])))
        #--Json to objects
        #++Check people with no tasks at this day
        try:                                                #Used, if a person has more than 1 task
            people.remove(task['people_id'])
        except:
            pass

    print(people)                                           #people now are all people with no task at specific date
    #--Check people with no tasks at that day

    #++Ifs *hust* AI to decide who gets Duty :3


    #--Ifs *hust* AI to decide who gets Duty :3

    #Send msg with duty-names
    msg = str(date) + "\n" + "" + duty1_str + "\n" + duty2_str + "\n" + tier2_str

    #Send alert to Slack, when duty is missing
    if(msg != ""):
        print(msg)
        web_hook_url = "https://hooks.slack.com/services/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"

        slack_msg = {'text':msg}

        requests.post(web_hook_url,data=json.dumps(slack_msg))

    #Get next date
    date = date + timedelta(days=1)  
