import requests
import json 
import yaml
import re


search_name = "appsec.live - pci was"
base_url = "https://cloud.tenable.com"
headers = {
  'X-ApiKeys': 'accessKey=e1fc5b82189a3e766d6cafe6b23b8e25b27ecf4c24e282096c0bd05778834ed7;secretKey=132e661fe60302dd58f1dbe063ea86a8f2553a7cb852fb9ff1a249ee2a4f4e9d',
}

yaml_path = "was_job.yaml"



def get_config_id():
    url=base_url+"/was/v2/configs/search"
    response = requests.request("POST", url, headers=headers)
    data=response.json()
    return data

def get_config_id_by_name(target_name,data):
    for item in data['items']:
        if item['name'] == target_name:
            return item['config_id']
    return None


def get_config(config_id):
    url=base_url+"/api/v3/export/configs/"+config_id
    response = requests.request("GET", url, headers=headers)
    data= response.text
    print(data)
    return data
    
data=get_config_id()
config_id = get_config_id_by_name(search_name,data)
conf_text=get_config(config_id).encode().decode("unicode_escape")



def str_presenter(dumper, data):
    if "\n" in data:  # sadece çok satırlı ise block scalar kullan
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

# Default str tipine bu davranışı tanıt
yaml.add_representer(str, str_presenter)




with open(yaml_path, 'r',encoding='utf-8') as f:
    yaml_docs = list(yaml.safe_load_all(f))

# ConfigMap bul, data.tenable_was.conf alanını güncelle
for doc in yaml_docs:
    if doc.get("kind") == "ConfigMap" and doc["metadata"]["name"] == "was-scanner-config":
        doc["data"] = {
            "tenable_was.conf": conf_text
        }

# Yeni YAML dosyasına yaz
with open("was-job-updated.yaml", "w",encoding='utf-8') as f:
    yaml.dump_all(yaml_docs, f, sort_keys=False,allow_unicode=True)


