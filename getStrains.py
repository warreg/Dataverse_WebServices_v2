from oauthlib.oauth2 import LegacyApplicationClient
from requests_oauthlib import OAuth2Session
from credentials import CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD,API_VERSION,SERVER_URL,TOKEN_URL
import requests
import json
import sys



def get_access_token():
    oauth = OAuth2Session(client=LegacyApplicationClient(client_id=CLIENT_ID))
    token = oauth.fetch_token(token_url=TOKEN_URL,
                              username=USERNAME,
                              password=PASSWORD,
                              client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET)

    access_token = token["access_token"]
    #print(access_token)
    return access_token


def define_headers():
    access_token = get_access_token()
    return {
        "accept": "application/json",
        "websiteId": "1",
        "Authorization": f"Bearer {access_token}",
    }

# def get_detail_url(record_id, api_version=None):
#         if api_version:
#             return "/".join([SERVER_URL, api_version, 'data',
#                              'WS Strains', str(record_id)])
#         else:
#             return "/".join([SERVER_URL, 'data', 'WS Strains', str(record_id)])

def get_detail_url(record_id, api_version=None):
        if api_version:
            return "/".join([SERVER_URL, api_version, 'summary',
                             'WS Strains', str(record_id)])
        else:
            return "/".join([SERVER_URL, 'summary', 'WS Strains', str(record_id)])


def get_strain_by_id(record_id):
        global json_file_name
        header = define_headers()
        url = get_detail_url(record_id, api_version=API_VERSION)
        response = requests.get(url, headers=header)

        if response.status_code == 200:
            print("********STARTING********")
            content = response.content
            json_dic = json.loads(content)
            for key in json_dic:
                if key == "Accession number":
                    #print(json_dic[key])
                    json_file_name = json_dic[key]

            with open(f"data/{json_file_name}.json","wb") as new_file:
                new_file.write(content)

            print(f"Step 1: GET STRAIN : {response.status_code}:{response.reason}")
            return json_file_name

        else:
            print(f"\nStep 1: ERROR  {response.status_code}:{response.reason} ")
            return False




#get_strain_by_id(8768767687878766)