import subprocess
import ast
import json
import requests
from credentials import API_TOKEN,PARENT,DATAVERSE_SERVER,MAJOR_OR_MINOR
import time


def create_dataset(js_file_name):
    file = f'uploads/{js_file_name}.json'

    curl = subprocess.Popen(f'curl -H "X-Dataverse-key:{API_TOKEN}" '
                     f'-X POST "{DATAVERSE_SERVER}/api/dataverses/{PARENT}/datasets" '
                     f'--upload-file "{file}"',shell=True,stdout=subprocess.PIPE)

    curl_return = curl.stdout.read()
    curl_str = curl_return.decode("UTF-8")
    curl_return_data = ast.literal_eval(curl_str)
    curl_return_doi = curl_return_data["data"]["persistentId"]
    time.sleep(1.0)
    return curl_return_doi

def upload_file(js_file_name):
    persistent_ID = create_dataset(js_file_name)

    with open(f"data/{js_file_name}.json","r") as op:
            dico = json.load(op)
            content = json.dumps(dico,indent=3)

    # Prepare "file"
    files = {'file': (f'{js_file_name}.json', content)}

    # Using a "jsonData" parameter, add optional description + file tags
    params = dict(description='strain json file')
    params_as_json_string = json.dumps(params)
    payload = dict(jsonData=params_as_json_string)

    # Add file using the Dataset's persistentId (e.g. doi, hdl, etc)
    url_persistent_id = '%s/api/datasets/:persistentId/add?persistentId=%s&key=%s' % (DATAVERSE_SERVER, persistent_ID, API_TOKEN)

    # Make the request
    r = requests.post(url_persistent_id, data=payload, files=files)

    # Print the response
    #print (r.status_code)
    time.sleep(1.0)
    return persistent_ID

def publish_dataset(js_file_name):
    persistent_ID = upload_file(js_file_name)
    curl =subprocess.Popen(f'curl -H "X-Dataverse-key:{API_TOKEN}" -X '
                           f'POST "{DATAVERSE_SERVER}/api/datasets/:persistentId/actions/:publish?persistentId={persistent_ID}&type={MAJOR_OR_MINOR}" ',
                           shell=True,stdout=subprocess.PIPE)

    curl_return = curl.stdout.read()
    curl_str = curl_return.decode("UTF-8")
    curl_return_data = ast.literal_eval(curl_str)
    curl_return_status = curl_return_data["status"]
    print(f"Step 3: PUBLISH DATASET : {curl_return_status}")
    print("*******COMPLETE*******")
    time.sleep(1.0)
