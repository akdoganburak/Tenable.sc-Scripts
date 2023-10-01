import string
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #SSL için çıkan uyarıları disable etme

#variable
sc_url=""
accesskey=""
secretkey=""
headers = {
    'x-apikey': 'accesskey='+accesskey+';secretkey='+secretkey,
    'X-ApiKeys': 'true'
    }

def getScan():
    response = requests.request("GET", sc_url+'/rest/scan', headers=headers,verify=False)
    data=response.json()['response']['usable']
    Scan_Id=[]
    rollover_scan_id=[]
    for key in data:
        Scan_Id.append(key['id'])
    for x in Scan_Id:
        response = requests.request("GET", sc_url+'/rest/scan/'+x, headers=headers,verify=False)
        data=response.json()['response']['schedule']
        if data["type"]=="rollover":
            rollover_scan_id.append(x)
    return rollover_scan_id

def deleteRolloverScan(rolloverscan):
    for x in rolloverscan:
        requests.request("DELETE", sc_url+'/rest/scan/'+x, headers=headers, verify=False)


rolloverscan=getScan()
deleteRolloverScan(rolloverscan)
    