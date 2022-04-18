import string
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import json


requests.packages.urllib3.disable_warnings(InsecureRequestWarning) #SSL için çıkan uyarıları disable etme

#variable
sc_url=""
accesskey=""
secretkey=""
asset_id=
query_id=


def getIP(): #Analysis kısmından belirli bir query'e göre ip listesi çekme fonksiyonu
    headers = {
        'User-Agent' : 'PostmanRuntime/7.29.0',
        'x-apikey': 'accesskey='+accesskey+ '; secretkey='+secretkey,
        'X-ApiKeys': 'true',
        'Content-Type': 'application/json',
        'Accept' : '*/*'
    }

    json_data = {
        'type': 'vuln',
        'query': {
            'id': query_id,
        },
        'sourceType': 'cumulative',
    }

    ip_list=''
    response = requests.post(sc_url+'/rest/analysis', headers=headers, json=json_data, verify=False)
    data=response.json()
    data1=data['response']['results']
    for key in data1:
            ip_list+=(key['ip'])+','
        
    ip_list=ip_list[:-1]
    return ip_list
    

def patchIP(ip: string): #ip listesini asset üzerinde değiştirme fonksiyonu
    headers = {
        'User-Agent' : 'PostmanRuntime/7.29.0',
        'x-apikey': 'accesskey='+accesskey+ '; secretkey='+secretkey,
        'X-ApiKeys': 'true',
        'Content-Type': 'application/json',
        'Accept' : '*/*'
    }

    json_data = {
        'type': 'static',
        'definedIPs': ip
    }

    response = requests.patch(sc_url+'/rest/asset/'+ str(asset_id), headers=headers, json=json_data, verify=False)
    print(response)


ip=getIP()
print(ip)
patchIP(ip)