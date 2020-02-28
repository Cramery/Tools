import requests
import json
from datetime import date, datetime, timedelta

endpoint = "https://api.float.com"
headers = {"Authorization": "Bearer 26df3bf128afcba2TolQQgadAEbqrEZ0xnxePuU9hBBgY6v7AGL0BDeEnzs"}

#Enter date
startdate = date(2020, 2, 26)
enddate = date(2020, 2, 29)

#Calculate numver of days
days = (enddate - startdate).days
date = startdate

#Get Data for each day
for i in range(0,days):
    #reset all duty-counters for this day
    duty1 = 0
    duty2 = 0
    tier2 = 0

    #get Data from Float API
    request = endpoint + "/v3/tasks?start_date=" + str(date) + "&end_date=" + str(date) 
    
    r = requests.get(request, headers=headers) 

    parsed_json = (json.loads(r.text))
    print(parsed_json)

    #Only interested in the names
    names = []

    for parsed in parsed_json:
        names.append(parsed['name'])

    #Count Duties on the day
    for name in names:
        if(name == "Duty 1"):
            duty1 = duty1 + 1
        if(name == "Duty 2"):
            duty2 = duty2 + 1
        if(name == "Tier 2"):
            tier2 = tier2 + 1

    print(str(date))
    print("Duty 1: " + str(duty1))  
    print("Duty 2: " + str(duty2))   
    print("Tier 2: " + str(tier2))
    print('\n')  

    #Calc if enough duties, if not, make a text
    msg = ""

    #Check if enough Duties
    if(duty1 < 2):
        msg = msg + str(2 - duty1) + " Duty 1 missing at " + str(date) + "\n"

    if(duty2 < 1):
        msg = msg + "Duty 2 missing at " + str(date) + "\n"
    
    if(tier2 < 1):
        msg = msg + "Tier 2 missing at " + str(date) + "\n"

    #Send alert to Slack, when duty is missing
    if(msg != ""):
        web_hook_url = "https://hooks.slack.com/services/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"

        slack_msg = {'text':msg}

        requests.post(web_hook_url,data=json.dumps(slack_msg))

    #Get next date
    date = date + timedelta(days=1)  
