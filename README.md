# MIRRI Dataverse WebServices


## Directories
:floppy_disk: The [data](data)  dir stores the raw data got from MIRRI-IS. 

:hammer_and_wrench: The [extra tools](extra_tools) dir contains script for launching the domain1.

:scroll: The [logs](logs) contains .... the logs :

:clipboard: The [templates](templates) dir contains json files that serve as standard models for creating dataset and also for PATCH Doi 

:open_file_folder: The [uploads](uploads) dir stores files ready to be uploaded into the dataverse :package: . 

## Process
The script is divided in essentialy 8 jobs :
1. **Get strain by ID**: data are got from MIRRI-IS by the [biolomics_client.py](biolomics_client.py)
2. **Get data values**: then data are extracted by [data_process.py](data_process.py) and stored in [data](data)
3. **Update template**: the template is updated by [data_process.py](data_process.py)
4. **Set dataset file**: and [data_process.py](data_process.py) create file  that will be used to create a dataset
5. **Create a dataset**: by the [dataverse_client.py](dataverse_client.py)
6. **Upload a file** : still with [dataverse_client.py](dataverse_client.py)     
7. **Publish the dataset**: with the [dataverse_client.py](dataverse_client.py)
8. **Patch the DOI**: by  [biolomics_client.py](biolomics_client.py)       


The [main.py](main.py) script performs all theses steps in a loop. 

The [resources.py](resources.py) contains dictionnaries 

The [settings.py](settings.py) contains all the credentials for performing connexion to MIRRIS-IS and dataverse API

A summary of the process is discribed in this [DataMIRRI_Diagrams.pdf](DataMIRRI_Diagrams.pdf). 


