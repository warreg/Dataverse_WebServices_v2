import json
from getStrains import get_strain_by_id

def prepare_strains(strain_ID):

    json_file_name = get_strain_by_id(strain_ID)

    if json_file_name == False:
        return False
    else:
        with open(f"data/{json_file_name}.json","r") as json_data:
            data_dict = json.load(json_data)
            ds_title = data_dict["Taxon name"][0]["Name"]
            ds_author_name = data_dict["Data provided by"]
            ds_author_affiliation = data_dict["Data provided by"]
            ds_contact_email = data_dict["Creator user name"]
            ds_contact_name = data_dict["Data provided by"]
            ds_description = data_dict["Restrictions on use"]

        with open("templates/dataset-template-sum.json","r") as json_template:
            template_dict = json.load(json_template)
            citation_fields_path = template_dict["datasetVersion"]["metadataBlocks"]["citation"]["fields"]
            #pprint(template_dict["datasetVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"])
            citation_fields_path[0]["value"] = ds_title
            citation_fields_path[1]["value"][0]["authorAffiliation"]["value"] = ds_author_affiliation
            citation_fields_path[1]["value"][0]["authorName"]["value"] = ds_author_name
            citation_fields_path[2]["value"][0]["datasetContactName"]["value"] = ds_contact_name
            citation_fields_path[2]["value"][0]["datasetContactEmail"]["value"] = ds_contact_email
            citation_fields_path[3]["value"][0]["dsDescriptionValue"]["value"] = ds_description
            # pprint(citation_fields_path[4]["value"][0])

        with open(f"uploads/{json_file_name}.json","w") as json_template:
            json_template.write(json.dumps(template_dict,indent=3))


        print("\nStep 2: PREPARE STRAIN: OK ")

        return json_file_name

#prepare_strains(76576576567575765)