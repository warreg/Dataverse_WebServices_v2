from settings import SERVER_URL,TOKEN_URL,CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD,API_VERSION,WEBSITE_ID
from settings import DATAVERSE_SERVER,API_TOKEN,PARENT,MAJOR_OR_MINOR,DIR_PATH
from biolomics_client import BiolomicsClient
from dataverse_client import DataverseClient
import data_process
import time
import logging.config
import os
import json



# LOGGING
logging.config.fileConfig(f"{DIR_PATH}/logs/logging.conf", disable_existing_loggers=False)
logger2 = logging.getLogger("log02")
logger3 = logging.getLogger("log03")

# BIOLOMICS CLIENT
bio_client = BiolomicsClient(CLIENT_ID, TOKEN_URL, USERNAME, PASSWORD, CLIENT_SECRET, SERVER_URL, API_VERSION, WEBSITE_ID)

# DATAVERSE CLIENT
dv_client = DataverseClient(DATAVERSE_SERVER, API_TOKEN, PARENT, MAJOR_OR_MINOR)

# CREATE & PUBLISH A DATASET
def define_new_dataset(record_id):
    """
    Retrieve json data for one Record_id and
    process data then create and publish dataset.
    return True/False result if dataset is published
    """

    # Getting the strain json file
    js_file = bio_client.get_strain_by_id(record_id)
    # Processing data
    data_values = data_process.get_data_values(js_file)
    template = data_process.update_template(data_values)
    dataset_file = data_process.set_metadata_file(js_file, template)
    # Create and publish dataset after uploading file
    doi = dv_client.create_dataset(dataset_file)
    upload_doi = dv_client.upload_file(dataset_file,doi)
    published = dv_client.publish_dataset(upload_doi)

    return {
        "record_name":f"{js_file}",
        "doi":f"{doi}",
        "published":f"{published}"
    }

# UPDATE A PUBLISHED DATASET
def update_dataset(record_id,doi):
    """
    update the dataset which the DOI is given in entry then
    performs all usual step for creating and publishing a dataset
    """

    logger2.info(f"PROCESSING RECORD ID {record_id}")

    js_file_update = bio_client.get_strain_by_id(record_id,update=True)
    data_values = data_process.get_data_values(js_file_update)
    metadatablocks = data_process.update_template(data_values, update=True)
    dataset_file = data_process.set_metadata_file(js_file_update, metadatablocks)
    updte = dv_client.update_new_metadata(dataset_file,doi)
    upload_file = dv_client.upload_file(dataset_file,doi)
    published = dv_client.publish_dataset(upload_file)


    return published

# SEND DOI TO MIRRI-IS AFTER DATASET PUBLICATION
def set_one_dataset(record_id):
    """
    This function carries out all the steps for creating a dataset
    then send the DOI to MIRRI-IS
    """

    time_0 = time.time()

    logger2.info(f"PROCESSING RECORD ID {record_id}")
    items_dir = os.path.join(DIR_PATH,"logs")
    items_file = "resume.log"

    record_id_str = f"{record_id}"
    patch = "False"

    with open(f"{items_dir}/{items_file}","r") as file:
        ID_db = json.load(file)

        if (record_id_str) not in ID_db.keys() or ID_db[record_id_str]["published"] == "False":

            new_dataset = define_new_dataset(record_id)
            doi = new_dataset["doi"]
            publi = new_dataset["published"]

            # Patch  DOI
            doi_dict = data_process.update_doi_template(doi)
            patch = bio_client.patch_doi(record_id, doi_dict, publi)

            # Send to logs
            timestp = time.time()

            tab_values = {
                "published" : publi,
                "doi" : doi,
                "timestp" : timestp
            }
            ID_db[record_id_str] = tab_values


        else:
            logger3.info("step 0 - Record_ID Already Processed")

    with open(f"{items_dir}/{items_file}","w") as file:
        json.dump(ID_db,file,indent=1)
    

    time_1 = time.time()
    duration = f"{(time_1 - time_0)//60} min {round((time_1 - time_0)%60,2)} sec"
    logger3.info(f'processed time: {duration}\n')

    return {
        "published":f"{patch}"
    }

# SAME OPERATION AS ABOVE IN A LOOP
def set_range_dataset(record_id, record_id_up):
    """
    Performs the @set_one_dataset func
    for all ID in a range
    """
    time_0 = time.time()
    logger3.info(f"{'='*75}")
    logger2.info(f"RUNNING RECORDS [{record_id} to {record_id_up}]\n")
    init_record = record_id
    processed = 0

    while record_id <= record_id_up:
        run = set_one_dataset(record_id)
        if run["published"] == "True":
            processed += 1
        record_id += 1

    time_1 = time.time()
    logger3.info(f"Processed records: [{record_id-init_record}/{record_id_up-init_record+1}] - Published: [{processed}/{record_id_up-init_record+1}]")
    logger3.info(f"Complete     time: {(time_1 - time_0)//60} min {round((time_1 - time_0)%60,2)} sec ")
    logger3.info(f"{'='*75}\n")

    return processed


# DEBUGGING LAUNCH PROD
def launch_debug():
    log_dir = os.path.join(DIR_PATH,"logs")
    file = "resume.log"
    false_tab = []

    with open(f"{log_dir}/{file}","r") as file:
        records_dic = json.load(file)

        for k, v in records_dic.items():
            if v["published"] ==  "False":
                false_tab += [int(k)]

    # for id in false_tab:
    #     set_one_dataset(id)



if __name__ == '__main__':

    #run = set_one_dataset(76515)
    set_range_dataset(105001,110000)
    #launch_debug()







# --
# "What doesn't kill us makes us stronger.	"

