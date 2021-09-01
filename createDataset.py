import subprocess
import ast
import json
import requests
from credentials import API_TOKEN,PARENT,DATAVERSE_SERVER,MAJOR_OR_MINOR
import os.path
import time
from prepareTemplate import update_dv_template

directory = os.path.dirname(__file__)

def create_dataset(js_file_name):
    if js_file_name == False:
        return False
    else:
        file_path_uploads = os.path.join(directory,"uploads",js_file_name)
        file = f'{file_path_uploads}.json'
        # file = f'uploads/{js_file_name}.json'

        curl = subprocess.Popen(f'curl -H "X-Dataverse-key:{API_TOKEN}" '
                         f'-X POST "{DATAVERSE_SERVER}/api/dataverses/{PARENT}/datasets" '
                         f'--upload-file "{file}"',shell=True,stdout=subprocess.PIPE)

        curl_return = curl.stdout.read()
        curl_str = curl_return.decode("UTF-8")
        curl_return_data = ast.literal_eval(curl_str)
        curl_return_status = curl_return_data["status"]
        if curl_return_status == "OK":
            curl_return_doi = curl_return_data["data"]["persistentId"]
            print(f"Step 3: CREATE DATASET: {curl_return_status}")
            return curl_return_doi
        else:
            print(f"Step 3 ERROR: CREATE DATASET {curl_str}")
            return False


def upload_file(js_file_name):
    """Function for uploading json file
    in the corresponding dataset"""

    if js_file_name == False:
        return False
    else:
        persistent_ID = create_dataset(js_file_name)

        if persistent_ID == False:
            return False
        else:
            file_path_data = os.path.join(directory,"data",js_file_name)
            with open(f"{file_path_data}.json","r") as op:
                    dico = json.load(op)
                    content = json.dumps(dico,indent=3)

            # with open(f"data/{js_file_name}.json","r") as op:
            #         dico = json.load(op)
            #         content = json.dumps(dico,indent=3)

            # Prepare "file"
            files = {'file': (f'{js_file_name}.json', content)}

            # Using a "jsonData" parameter, add optional description + file tags
            params = dict(description='Strain json file')
            params_as_json_string = json.dumps(params)
            payload = dict(jsonData=params_as_json_string)

            # Add file using the Dataset's persistentId (e.g. doi, hdl, etc)
            url_persistent_id = f"{DATAVERSE_SERVER}/api/datasets/:persistentId/add?persistentId={persistent_ID}&key={API_TOKEN}"

            # Make the request
            resp = requests.post(url_persistent_id, data=payload, files=files)

            if resp.status_code == 200:
                print(f"Step 4: UPLOADING FILE : {resp.status_code}:{resp.reason}")
                return persistent_ID
            else:
                print(f"Step 4: ERROR: UPLOADING FILE: {resp.status_code}:{resp.reason}")
                return False



def publish_dataset(js_file_name):

    if js_file_name == False:
        return False
    else:
        persistent_ID = upload_file(js_file_name)

        if persistent_ID == False:
            return False
        else:
            curl =subprocess.Popen(f'curl -H "X-Dataverse-key:{API_TOKEN}" -X '
                                   f'POST "{DATAVERSE_SERVER}/api/datasets/:persistentId/actions/:publish?persistentId={persistent_ID}&type={MAJOR_OR_MINOR}" ',
                                   shell=True,stdout=subprocess.PIPE)

            curl_return = curl.stdout.read()
            curl_str = curl_return.decode("UTF-8")
            curl_return_data = ast.literal_eval(curl_str)
            curl_return_status = curl_return_data["status"]
            if curl_return_status == "OK":
                print(f"Step 5: PUBLISH DATASET: {curl_return_status} \n\n")
                return curl_return_status
            else:
                print(f"Step 5: ERROR: PUBLISH DATASET : {curl_str} ")
                return False


################################################################
#
# js_file = update_dv_template(45)
# create_dataset(js_file)