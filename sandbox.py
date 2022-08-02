from settings import DIR_PATH,API_TOKEN,DATAVERSE_SERVER
import subprocess
import os.path
import requests
import traceback
import json


# UPDATE METADATA
def get_metadata_schema(js_file,doi):
    update_dir = os.path.join(DIR_PATH,"updates")
    file_path = f'{update_dir}/{js_file}'

    headers = {'X-Dataverse-key': f"{API_TOKEN}",}
    response = requests.get(f'{DATAVERSE_SERVER}/api/datasets/:persistentId/versions/:latest?persistentId={doi}',
                            headers=headers)

    content = response.content
    json_loads = json.loads(content)
    metadata_blocks = {}
    # Define "metadataBlocks" as key for json object so as to fit for schema to update command
    metadata_blocks["metadataBlocks"] = json_loads["data"]["metadataBlocks"]

    with open(f"{file_path}_metadata_schema.json","w") as f:
        f.write(json.dumps(metadata_blocks,indent=3))

    print(response.status_code)


def edit_metadata_schema(file_to_update):
    # get the new values to updates
    # process new metadata schema
    pass

def update_new_metadata(doi):
    curl = subprocess.Popen(f'curl -H "X-Dataverse-key: {API_TOKEN}"'
                     f' -X PUT {DATAVERSE_SERVER}/api/datasets/:persistentId/versions/:draft?persistentId={doi}'
                     f' --upload-file {DIR_PATH}/updates/MIRRI0000001.json',
                     shell=True,stdout=subprocess.PIPE)

    curl_return = curl.stdout.read()
    curl_str = curl_return.decode("UTF-8")

    if curl_str:
        curl_dict = json.loads(curl_str)
        print(curl_dict["data"]["datasetPersistentId"])
            # status = curl_dict['status']
            #
            # if status:
            #     print(curl_dict)
            # else:
            #     print("Nothing else")
    else:
        print("Something wrong")


def publish_new_metadata(doi):
    # utiliser un decorateur ???
    pass

# DELETE DATASET
def delete_unpublished_dataset(doi):
    # Get the dataset ID first
    headers = {'X-Dataverse-key': f"{API_TOKEN}",}
    def get_dataset_id(doi):
        response = requests.get(f'{DATAVERSE_SERVER}/api/datasets/:persistentId/?persistentId={doi}',
                                headers=headers)
        json_response = response.json()
        dataset_id = json_response["data"]["id"]
        return dataset_id

    # Then delete the dataset with its ID
    dataset_id = get_dataset_id(doi)
    response = requests.delete(f'{DATAVERSE_SERVER}/api/datasets/{dataset_id}', headers=headers)

    return response.status_code

def delete_dataset(doi):
    global response
    headers = {'X-Dataverse-key': f"{API_TOKEN}",}
    try:
        response = requests.delete(f'{DATAVERSE_SERVER}/api/datasets/:persistentId/destroy/?persistentId={doi}',
                               headers=headers, timeout=25)
    except requests.exceptions.ReadTimeout:
        print("Timeout")
    except:
        print(f"step 6 - {traceback.format_exc(0)}")
    else:
        if response.status_code == 200:
            print("ok")
        else:
            print("Wrong")

    return response.status_code


#update_new_metadata("doi:10.21386/FK2/MPDZ2Z")
#delete_unpublished_dataset("doi:10.21386/FK2/UGBWPD")
#delete_dataset("doi:10.21386/FK2/RZMG9H")

update_new_metadata("doi:10.82062/MIRRI/0VLAJ8")