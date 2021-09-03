import json
from getStrains import get_strain_by_id
import os.path
import logging
import time

# Create log file for errors
logging.basicConfig(
    level=logging.ERROR,
    filename="logs/err.log",
    format='%(asctime)s %(name)s %(levelname)s:%(message)s')

logger = logging.getLogger(__name__)


def update_dv_template(strain_ID):
    """Function for preparing template to upload json file"""

    json_file_name = get_strain_by_id(strain_ID)

    if json_file_name == False:
        print("Step 2: ERROR: on PREPARE TEMPLATE ! ")
        return False
    else:
        directory = os.path.dirname(__file__)
        file_path_data = os.path.join(directory,"data",json_file_name)
        file_path_template = os.path.join(directory,"templates","dataset-template-sum.json")
        file_path_uploads = os.path.join(directory,"uploads",json_file_name)

        with open(f"{file_path_data}.json","r") as json_data:
            data_dict = json.load(json_data)

            # Formatting data_dict for log file
            data_dict_log = json.dumps(data_dict,indent=3)

            try:
                ds_title = data_dict["Taxon name"][0]["Name"]
                ds_author_name = data_dict["Data provided by"]
                ds_author_affiliation = data_dict["Data provided by"]
                ds_contact_email = data_dict["Creator user name"]
                ds_contact_name = data_dict["Data provided by"]
                ds_description = data_dict["Restrictions on use"]
            except IndexError:
                # write err in err.log file
                logger.error(f"\n\nindex error in {json_file_name}.json \n {data_dict_log} ")
                return False
            else:
                # Fill in the template
                with open(f"{file_path_template}","r") as json_template:
                    template_dict = json.load(json_template)
                    citation_fields_path = template_dict["datasetVersion"]["metadataBlocks"]["citation"]["fields"]
                    citation_fields_path[0]["value"] = ds_title
                    citation_fields_path[1]["value"][0]["authorAffiliation"]["value"] = ds_author_affiliation
                    citation_fields_path[1]["value"][0]["authorName"]["value"] = ds_author_name
                    citation_fields_path[2]["value"][0]["datasetContactName"]["value"] = ds_contact_name
                    citation_fields_path[2]["value"][0]["datasetContactEmail"]["value"] = ds_contact_email
                    citation_fields_path[3]["value"][0]["dsDescriptionValue"]["value"] = ds_description
                    # pprint(citation_fields_path[4]["value"][0])

                    with open(f"{file_path_uploads}.json","w") as json_template:
                        json_template.write(json.dumps(template_dict,indent=3))


                print("Step 2: PREPARE TEMPLATE: OK ")

                return json_file_name

update_dv_template(2072)
#update_dv_template(76576576567575765)
# begin = time.time()
# id = 10
# while id <= 10:
#     update_dv_template(id)
#     id += 1
# end = time.time()
# duration = end  - begin
# if duration >= 60:
#     print(f"Complete time : {duration//60} min {round(duration%60,2)} sec")
# else:
#     print(f"Complete time : {round(duration,2)} sec")