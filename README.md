# Tools
Random Tools, Skripts and Stuff I coded. Most of them bc I'm a lazy shithead.

**Check Duties:**

Get Data from Float-Planning tool. Check how many Duties from each type are planned at a specific date. Inform over Slack if Duties are missing

How-To use:

Enter Start- and Enddate of timerange, when it should be checked
```
#Enter date
startdate = date(2020, 2, 26)
enddate = date(2020, 2, 29)
```

Enter Access_Key to Float
```
headers = {"Authorization": "Bearer <Access Key>"}
```

Change Webhook URL for your Slack channel
```
web_hook_url = "webhook_url"
```
