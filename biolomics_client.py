import traceback
import requests
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import LegacyApplicationClient
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError
import json
import os
import time
from settings import DIR_PATH
import logging.config


#from credentials import CLIENT_ID,TOKEN_URL,USERNAME,PASSWORD,CLIENT_SECRET,SERVER_URL,API_VERSION,WEBSITE_ID

logging.config.fileConfig(f"{DIR_PATH}/logs/logging.conf", disable_existing_loggers=False)
logger2 = logging.getLogger("log02")
logger3 = logging.getLogger("log03")


class BiolomicsClient:
    """
    This class aims to connect to Biolomics webservices
    and retrieve data from it
    """
    def __init__(self, client_id, token_url, username, password, client_secret, server_url, api_version, website_id):
        self.client_id = client_id
        self.token_url = token_url
        self.username = username
        self.password = password
        self.client_secret = client_secret
        self.server_url = server_url
        self.api_version = api_version
        self.website_id = website_id
        self.client = None


    def get_access_token(self):
        """
        getting access token to connect to webservices
        :return: access token
        """
        try:
            if self.client is None:
                self.client = LegacyApplicationClient(client_id=self.client_id)
                authenticated = False
            else:
                expires_at = self.client.token["expires_at"]
                authenticated = expires_at > time.time()
            if not authenticated:
                oauth = OAuth2Session(client=self.client)
                try:
                    token = oauth.fetch_token(
                        token_url=self.token_url,
                        username=self.username,
                        password=self.password,
                        client_id=self.client_id,
                        client_secret=self.client_secret
                    )
                except InvalidGrantError:
                    oauth.close()
                    raise

                self.access_token = token["access_token"]
                oauth.close()
        except:
            return None
        else:
            return self.access_token


    def define_get_headers(self):
        """
        :returns the headers for the GET request
        """
        access_token = self.get_access_token()

        if access_token is not None :
            return {
                "accept": "application/json",
                "websiteId": f"{self.website_id}",
                "Authorization": f"Bearer {access_token}"
            }

        else:
            return None


    def get_url(self, record_id, api_version=None):
        """
        Using the data endpoint for getting  full records
        :param record_id: the accession number
        :param api_version: the biolomics webservice version
        :return: data endpoint url
        """
        url_tab = {}
        if api_version:
            summary_url = "/".join([self.server_url, api_version, 'summary',
                             'WS Strains', str(record_id)])

            data_url = "/".join([self.server_url, api_version, 'data',
                             'WS Strains', str(record_id)])

            url_tab["summary_url"] = summary_url
            url_tab["data_url"] = data_url

        else:
            summary_url = "/".join([self.server_url, 'summary',
                             'WS Strains', str(record_id)])

            data_url = "/".join([self.server_url, 'data',
                             'WS Strains', str(record_id)])

            url_tab["summary_url"] = summary_url
            url_tab["data_url"] = data_url

        return url_tab


    def get_strain_by_id(self, record_id, update=False):
        """
        Sending an GET request and download a json file response into /data dir
        :param update: if there is an new insert or update
        :param record_id: the accession number
        :return: the name of the file downloaded
        """
        global json_file_name
        #=======================
        url_tab = self.get_url(record_id, api_version=self.api_version)
        url = url_tab["data_url"]
        #=======================

        header = self.define_get_headers()
        #logger2.info(f"PROCESSING RECORD ID {record_id}")

        if header is not None:
            try:
                response = requests.get(url, headers=header,timeout=25)
            except requests.exceptions.ReadTimeout:
                logger3.info("step 1 : Err 2 - timeout exceeded ")
                json_file_name = None
            except:
                logger3.error(f"step 1 : Err 3 - {traceback.format_exc(0)}")
                json_file_name = None
            else:
                if response.status_code == 200:
                    try:
                        content = response.content
                        json_dic = json.loads(content)

                        for key in json_dic:
                            if key == "RecordName":
                                if update == True:
                                    json_file_name = f"{json_dic[key]}_updated"
                                else:
                                    json_file_name = json_dic[key]

                        data_dir = os.path.join(DIR_PATH, "data")
                        json_file = f"{json_file_name}.json"

                        with open(f"{data_dir}/{json_file}","wb") as new_file:
                            new_file.write(content)

                        logger3.info(f"step 1 - GET STRAIN BY ID: {response.reason}")
                    except:
                        logger3.error(f"step 1 : Err 5 - {traceback.format_exc(0)}")
                        json_file_name = None

                else:
                    #print(f"step 1 - GET STRAIN BY ID: Error retrieving data: {response.status_code} {response.reason}")
                    logger3.info(f"step 1 : Err 4 - Error retrieving data: {response.status_code} {response.reason}")
                    json_file_name = None

            return json_file_name

        else:
            #print("step 1 - GET STRAIN BY ID: Error establishing connexion !")
            logger3.info("step 1 : Err 1 - Error establishing connexion !")
            return None # or False

    def define_patch_headers(self):
        """
        :returns the headers for the PATCH request
        """
        access_token = self.get_access_token()

        if access_token is not None :
            return {
                "Content-type": "application/json",
                "websiteId": f"{self.website_id}",
                "Authorization": f"Bearer {access_token}"
            }

        else:
            return None

    def patch_doi(self,record_id,doi_dic,published):
        """
        send the DOI got from the published dataset
        to the corresponding strains in MIRRI-IS
        :return: a True/False if success
        """

        url_tab = self.get_url(record_id)
        url = url_tab["data_url"]

        payload = doi_dic
        header = self.define_patch_headers()
        if published == "True":
            try:
                response = requests.patch(url, json.dumps(payload), headers=header, timeout=25)
            except requests.exceptions.ReadTimeout:
                logger3.info("step 8 - Err 2: timeout exceeded")
                patch = "False"
            except:
                logger3.error(f"step 8 - Err 3: {traceback.format_exc(0)}")
                patch = "False"
            else:
                if response.status_code == 200:
                    logger3.info("step 8 - PATCH DOI:        OK")
                    patch = "True"
                else:
                    logger3.info("step 8 - Err 4: status code != 200")
                    patch = "False"

        else:
            logger3.info("step 8 - Err 1: None")
            patch = "False"

        return patch




# --
# "Life is like a box of chocolates. You never know  what you’re gonna get". Forrest Gump