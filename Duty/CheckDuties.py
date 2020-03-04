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


#++Globals
endpoint = "https://api.float.com"
headers = {"Authorization": "Bearer "}

#Enter date
startdate = date(2020, 3, 2)
enddate = date(2020, 3, 6)

#Calculate numver of days
days = (enddate - startdate).days
days = days + 1
date = startdate
##--Globals

#Get Tasks for each day
for i in range(0,days):
    #reset all duty-counters for this day
    duty1 = 0
    duty2 = 0
    tier2 = 0

    #get Data from Float API
    request = endpoint + "/v3/tasks?start_date=" + str(date) + "&end_date=" + str(date) 
    
    r = requests.get(request, headers=headers) 

    tasks_json = (json.loads(r.text))
    
    #++Json to objects
    tasks = []

    for task in tasks_json:
        tasks.append(Task((task['task_id']), (task['name']), (task['people_id']), (task['project_id'])))
        
    #--Json to objects

    #Count Duties on the day
    for task in tasks:
        if(task.project_id == 1947241):
            duty1 = duty1 + 1
        if(task.project_id == 1947243):
            duty2 = duty2 + 1
        if(task.project_id == 1906635):
            tier2 = tier2 + 1

    print(str(date))
    print("Duty 1: " + str(duty1))  
    print("Duty 2: " + str(duty2))   
    print("Tier 2: " + str(tier2) + '\n')

    #Calc if enough duties, if not, make a text
    msg = ""

    #Check if enough Duties
    if(duty1 < 2):
        msg = msg + str(date) + ": " + str(2 - duty1) + " Duty 1 missing" + "\n"

    if(duty2 < 1):
        msg =  msg + str(date) + ": Duty 2 missing" + "\n"
    
    if(tier2 < 1):
        msg = msg + str(date) + ": Tier 2 missing" + "\n"

    if((duty1 >= 2)and(duty2 >= 1)and(tier2 >= 1)):
        msg = msg + str(date) + ": Enough Duties" + "\n"
    
    #Send alert to Slack, when duty is missing
    if(msg != ""):
        
        web_hook_url = "https://hooks.slack.com/services/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"

        slack_msg = {'text':msg}

        requests.post(web_hook_url,data=json.dumps(slack_msg))

    #Get next date
    date = date + timedelta(days=1)  
