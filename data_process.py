import json
import os.path
from settings import DIR_PATH,DATAVERSE_SERVER
from resources import DISPLAY_LINK,CONTACTS,VOCABULAR
import logging.config
import traceback

# LOGGING
logging.config.fileConfig(f"{DIR_PATH}/logs/logging.conf", disable_existing_loggers=False)
logger3 = logging.getLogger("log03")
logger4 = logging.getLogger("log04")


def recuperator(field):
    """
    Designed mostly for "Form" and "Organism type" values;
    this func return the item value where there is dift to "?"
    """
    field_value_tab = field["Value"] # tab
    res = ""
    for item in field_value_tab:
        if item["Value"] != "?":
            res = item["Name"]
            # In case there maybe several values
            # res += " "+item["Name"]
    return res


def get_data_values(js_file):
    """
    Opens the last json file in /data dir
    got by biolomics_client and get raw values from it
    :return: values dictionary
    """
    if js_file is not None:
        json_file = f"{js_file}.json"
        data_dir = os.path.join(DIR_PATH,"data")
        data_values = {}

        # Get the data values
        with open(f"{data_dir}/{json_file}","r") as data_file:
            data_dict = json.load(data_file)

            try:
                record_details = data_dict["RecordDetails"]

                delivery_form = recuperator(record_details["Form"])
                organism_type = recuperator(record_details["Organism type"])
                collection = record_details["Data provided by"]["Value"]

                # From MIRRI WS
                data_values["delivery_form"] = delivery_form
                data_values["organism_type"] = organism_type #4
                contact_email = ""

                # Retrieve contact emails from resource/CONTACT
                try:
                    if collection not in CONTACTS.keys():
                        CONTACTS[collection] = "info@mirri.org"
                except KeyError:
                    pass

                for catalog, email in CONTACTS.items():
                    if catalog == collection:
                        contact_email = email
                        if email ==  "":
                            contact_email = "info@mirri.org"
                    else:
                        contact_email = "info@mirri.org"

                # Bypass the IndexError that occurs when country field is empty
                try:
                    country = record_details["Country"]["Value"][0]["Name"]["Value"]
                except IndexError:
                    country = ""


                # ************
                vocab_link = ""
                microorg_link = ""
                microorg_vocab =""

                for vocab,link in VOCABULAR.items():
                    if vocab == organism_type:
                        vocab_link = link
                    if vocab == "Microorganism":
                        microorg_link = link
                        microorg_vocab = vocab

                data_values["microorg_vocab"] = microorg_vocab
                data_values["microorg_link"] = microorg_link
                data_values["vocab_link"] = vocab_link
                # ************

                # From MIRRI WS
                data_values["taxon_name"] = record_details["Taxon name"]["Value"][0]["Name"]["Value"] #1
                # data_values["author"] = record_details[""] # ???
                # data_values["year"] = record_details[""] # ???
                data_values["nagoya"] = record_details["Nagoya protocol restrictions and compliance conditions"]["Value"]
                data_values["restrictions"]= record_details["Restrictions on use"]["Value"]
                data_values["risk_group"] = record_details["Risk group"]["Value"]
                data_values["country"] = country #4
                data_values["geographic_origin"] = record_details["Geographic origin"]["Value"]
                data_values["collector"] = record_details["Collector"]["Value"]
                #data_values["collection_date"] = record_details["Collection date"]["Value"]
                data_values["isolator"] = record_details["Isolator"]["Value"]
                data_values["isolation_date"] = record_details["Isolation date"]["Value"]
                data_values["depositor"] = record_details["Depositor"]["Value"]
                data_values["deposit_date"] = record_details["Deposit date"]["Value"]
                data_values["provided_by"] = collection #2
                data_values["collection_access_number"] = record_details["Collection accession number"]["Value"] #4
                #data_values["growth_medium"] = record_details["Recommended growth medium"]["Value"][0]["Name"]["Value"]
                data_values["growth_temp"] = record_details["Recommended growth temperature"]["MaxValue"]
                data_values["record_id"] = data_dict["RecordId"] # equivalent accession_number_strip
                data_values["record_name"] = data_dict["RecordName"] #1 #4
                #data_values["creator"] = data_dict["CreatorUserName"]
                data_values["contact_email"] = contact_email #3


            except KeyError:
                logger4.error(f"Key Error in {js_file}.json ")
                logger3.error(f"step 2 - Err 2: {traceback.format_exc(0)}")
                data_values = None
            except:
                logger4.error(f"{traceback.format_exc(0)} in {js_file}")
                logger3.error(f"step 2 - Err 3: {traceback.format_exc(0)}")
                data_values = None
            else:
                logger3.info("step 2 - GET DATA VALUES:  OK")

        #print("step 2 - GET DATA VALUES: OK")

        return data_values

    else:
        logger3.info("step 2 - Err 1: None")
        return None


def update_template(data_values, update=False):
    """
    Replace the template values (dataset-template.json) by
    values dictionary obtained by @get_data_vales()
    :param update:
    """
    if data_values is not None:
        try:
            template_dir = os.path.join(DIR_PATH,"templates")
            template_file = "dataset-template-sum.json"

            with open(f"{template_dir}/{template_file}","r") as json_template:
                template_dict = json.load(json_template)

                # ************* FOR UPDATE *************
                metadata_blocks = {}
                metadata_blocks["metadataBlocks"] = template_dict["datasetVersion"]["metadataBlocks"]
                # **************************************

                citation_fields = template_dict["datasetVersion"]["metadataBlocks"]["citation"]["fields"]

                # ========== If country empty: don't mention it in description =================

                if data_values["country"] == "":
                    description = f'' \
                                                                                f'Organism type: {data_values["organism_type"]} ;  ' \
                                                                                f'Taxon name: {data_values["taxon_name"]} ;  ' \
                                                                                f'Collection: {data_values["collection_access_number"]}   '
                else:
                    description = f'' \
                                                                                f'Organism type: {data_values["organism_type"]} ;  ' \
                                                                                f'Taxon name: {data_values["taxon_name"]} ;  ' \
                                                                                f'Collection: {data_values["collection_access_number"]} ;  ' \
                                                                                f'Country: {data_values["country"]} '
                # ===============================================================================

                # Title
                citation_fields[0]["value"] = f'{data_values["record_name"]}'
                # Alternative URL
                citation_fields[1]["value"] = f"{DISPLAY_LINK}{data_values['record_id']}"
                # Author Affiliation
                citation_fields[2]["value"][0]["authorAffiliation"]["value"] = data_values["provided_by"]
                # Author name
                citation_fields[2]["value"][0]["authorName"]["value"] = data_values["provided_by"]
                # Contact Name
                citation_fields[3]["value"][0]["datasetContactName"]["value"] = data_values["provided_by"]
                # Contact Email
                citation_fields[3]["value"][0]["datasetContactEmail"]["value"] = data_values["contact_email"]
                # Description
                citation_fields[4]["value"][0]["dsDescriptionValue"]["value"] = description
                # Microorganism keyword
                citation_fields[6]["value"][0]["keywordValue"]["value"] = data_values["microorg_vocab"]
                # Microorganism keyword vocabulary
                citation_fields[6]["value"][0]["keywordVocabularyURI"]["value"] = data_values["microorg_link"]
                # Keyword
                citation_fields[6]["value"][1]["keywordValue"]["value"] = data_values["organism_type"]
                # Keyword vocabulary
                citation_fields[6]["value"][1]["keywordVocabularyURI"]["value"] = data_values["vocab_link"]

            #print("step 3: updates template OK")
            logger3.info("step 3 - UPDATE TEMPLATE:  OK")
        except:
            logger3.error(f"step 3 - Err 2: {traceback.format_exc(0)}")
            template_dict = None

        if update == True:
            return metadata_blocks
        else:
            return template_dict
    else:
        logger3.info("step 3 - Err 1: None")
        return None


def set_metadata_file(js_file, template_dict):
    """
    Create new dataset template file  in
    /uploads dir that will be used to create dataset
    """
    if (js_file is not None) & (template_dict is not None):
        try:
            uploads_dir = os.path.join(DIR_PATH,"uploads")
            uploads_file = f"{js_file}.json"

            with open(f"{uploads_dir}/{uploads_file}","w") as upload:
                upload.write(json.dumps(template_dict,indent=3))

            #print("step 4: set_metadata_file OK")
            logger3.info("step 4 - SET DATASET FILE: OK")
        except:
            logger3.error(f"step 4 - Err 2: {traceback.format_exc(0)}")
            js_file = None

        return js_file
    else:
        logger3.info("step 4 - Err 1: None")
        return None


def update_doi_template(doi):
    """
    replace the DOI template values by the values from published dataset
    """
    template_dir = os.path.join(DIR_PATH,"templates")
    template_file = "patch-doi-template.json"
    doi_link = f"{DATAVERSE_SERVER}/dataset.xhtml?persistentId={doi}"

    with open(f"{template_dir}/{template_file}","r") as json_template:
        template_dict = json.load(json_template)
        doi_field = template_dict["RecordDetails"]["Dataverse DOI"]["Value"][0]
        doi_field["Value"] = doi_link
        doi_field["name"] = doi

    return template_dict



# --
# "Life is like riding a bicycle. To keep your balance, you must keep moving." Albert Einstein