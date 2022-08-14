import subprocess
import ast
import json
import requests
import os.path
from settings import DIR_PATH
import logging.config
import traceback

logging.config.fileConfig(f"{DIR_PATH}/logs/logging.conf", disable_existing_loggers=False)
logger3 = logging.getLogger("log03")


class DataverseClient:
    """
    This class aims to create datasets using @BiolomicsClient
    and @data_process, then upload files and publish it
    """

    def __init__(self,dataverse_server, api_token, parent, major_or_minor):
        self.dataverse_server = dataverse_server
        self.api_token = api_token
        self.parent = parent
        self.major_or_minor = major_or_minor

    # CREATE A DATASET
    def create_dataset(self,js_file):
        """
        Use dataverse API to create a dataset
        by using the last upload file as template
        for fill in metadata
        """
        if js_file is not None:
            uploads_dir = os.path.join(DIR_PATH,"uploads")
            file = f'{uploads_dir}/{js_file}.json'

            curl = subprocess.Popen(f'curl --max-time 25 -H "X-Dataverse-key:{self.api_token}" '
                             f'-X POST "{self.dataverse_server}/api/dataverses/{self.parent}/datasets" '
                             f'--upload-file "{file}" -H "Content-type:application/json" ',shell=True,stdout=subprocess.PIPE)

            curl_return = curl.stdout.read()
            curl_str = curl_return.decode("UTF-8")
            #print(curl_str)

            if curl_str:
                curl_return_data = ast.literal_eval(curl_str)
                curl_return_status = curl_return_data["status"]


                if curl_return_status == "OK":
                    doi = curl_return_data["data"]["persistentId"]
                    logger3.info("step 5 - CREATE DATASET:   OK")
                else:
                    logger3.error(f"step 5 - Err 3: {traceback.format_exc(0)}")
                    doi = None
                    #print(curl_return_status)

            else:
                logger3.info(f"step 5 - Err 2: {traceback.format_exc(0)}")
                doi = None

            return doi

        else:
            logger3.info("step 5 - Err 1: None")
            return  None

    # UPDATE DATASET
    def update_new_metadata(self,js_file_updated,doi):
        """
        update a dataset already published
        """

        if js_file_updated is not None:
            uploads_dir = os.path.join(DIR_PATH,"uploads")
            file = f'{uploads_dir}/{js_file_updated}.json'

            curl = subprocess.Popen(f'curl -H "X-Dataverse-key: {self.api_token}"'
                             f' -X PUT {self.dataverse_server}/api/datasets/:persistentId/versions/:draft?persistentId={doi}'
                             f' --upload-file {file}',
                             shell=True,stdout=subprocess.PIPE)

            curl_return = curl.stdout.read()
            curl_str = curl_return.decode("UTF-8")

            if curl_str:
                curl_dict = json.loads(curl_str)
                curl_status = curl_dict["status"]

                if curl_status == "OK":
                    doi = curl_dict["data"]["datasetPersistentId"]
                    logger3.info("step 5 - UPDATE DATASET:   OK")
                else:
                    logger3.error(f"step 5 - Err 3: {traceback.format_exc(0)}")
                    doi = None

            else:
                logger3.info(f"step 5 - Err 2: {traceback.format_exc(0)}")
                doi = None

            return doi

        else:
            logger3.info("step 5 - Err 1: None")
            return  None

    # UPLOAD FILE IN A DATASET
    def upload_file(self,js_file, doi):
        """
        Upload the json file in /data dir into the new dataset created
        :param doi: the doi request response in @create_dataset
        """
        if (js_file is not None) & (doi is not None):
            json_file = f"{js_file}.json"
            data_dir = os.path.join(DIR_PATH,"data")

            with open(f"{data_dir}/{json_file}","r") as data_file:
                data_dict = json.load(data_file)
                content = json.dumps(data_dict,indent=3)

            files = {'file': (f'{js_file}.json', content)}
            # Using a "jsonData" parameter, add optional description + file tags
            params = dict(description='Strain json file')
            params_as_json_string = json.dumps(params)
            payload = dict(jsonData=params_as_json_string)
            # Add file using the Dataset's persistentId
            url_persistent_id = f"{self.dataverse_server}/api/datasets/:persistentId/add?persistentId={doi}&key={self.api_token}"
            # Make the request
            try:
                resp = requests.post(url_persistent_id, data=payload, files=files, timeout=25)
            except requests.exceptions.ReadTimeout:
                logger3.info("step 6 - Err 2: timeout exceeded")
                doi = None
            except:
                logger3.error(f"step 6 - Err 3: {traceback.format_exc(0)}")
                doi = None
            else:
                if resp.status_code == 200:
                    #print("step 6: upload file OK")
                    logger3.info("step 6 - UPLOAD FILE:      OK")
                else:
                    logger3.info("step 6 - Err 4: status code != 200")
                    doi = None
            return doi
        else:
            logger3.info("step 6 - Err 1: None")
            return None

    # PUBLISH A DATASET
    def publish_dataset(self,doi):
        """
        Performs dataverse API to publish the dataset
        created in @create_dataset and check the request response
        """
        if doi is not None:
            curl = subprocess.Popen(f'curl --max-time 25 -H "X-Dataverse-key:{self.api_token}" -X '
                                       f'POST "{self.dataverse_server}/api/datasets/:persistentId/actions/:publish?persistentId={doi}&type={self.major_or_minor}" ',
                                       shell=True,stdout=subprocess.PIPE)

            curl_return = curl.stdout.read()
            curl_str = curl_return.decode("UTF-8")

            if curl_str:
                curl_return_data = ast.literal_eval(curl_str)
                curl_return_status = curl_return_data["status"]

                if curl_return_status == "OK":
                    published = True
                    #print("step 7: publish dataset OK")
                    logger3.info("step 7 - PUBLISH DATASET:  OK")
                else:
                    logger3.info("step 7 - Err 3: response status code  != 200")
                    published = False
            else:
                logger3.error(f"step 7 - Err 2: {traceback.format_exc(0)}")
                published = False

            return published
        else:
            logger3.info("step 7 - Err 1: None")
            return False



# --
# "Speak softly and carry a big stick" Theodore Roosevelt