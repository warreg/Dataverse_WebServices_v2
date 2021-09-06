from prepareTemplate import update_dv_template
from createDataset import publish_dataset
import time
import sys
from datetime import datetime
import logging


# Create log file for errors
# logging.basicConfig(
#     level=logging.ERROR,
#     filename="logs/inf.log",
#     format='%(asctime)s %(name)s %(levelname)s:%(message)s')
#
# logger = logging.getLogger(__name__)


def set_singl_dataset(record_ID):
    json_file_name = update_dv_template(record_ID)
    if json_file_name == False:
        sys.exit("Oups !")
    else:
        publish_dataset(json_file_name)


def set_multi_dataset(record_ID,record_ID_max):
    record_init = record_ID
    while record_ID <= record_ID_max :
        print(f"\nExecuting: record >>> {record_ID} ")
        json_file_name = update_dv_template(record_ID)
        publish_dataset(json_file_name)
        record_ID += 1
    print(f"Processed records: {(record_ID_max - record_init)+1}")



if __name__ == '__main__':
    begin = time.time()
    id_1 = 3000
    id_2 = 8000
    set_multi_dataset(id_1,id_2)
    #set_singl_dataset(9865)
    end = time.time()
    duration = end  - begin

    print(f"\nComplete time : {duration//60} min {round(duration%60,2)} sec")

    with open("logs/inf.log","a") as log_f:
        log_f.write(f"\n{datetime.now()}: "
                    f"ID_Records: {id_1}-{id_2} [{(id_2-id_1)+1} records]  "
                    f"Total duration: {duration//60} min {round(duration%60,2)} sec ")
