from prepareTemplate import update_dv_template
from createDataset import publish_dataset
import time
import sys



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
    set_multi_dataset(2000,7000)
    #set_singl_dataset(9865)
    end = time.time()
    duration = end  - begin
    if duration >= 60:
        print(f"\nComplete time : {duration//60} min {round(duration%60,2)} sec")
    else:
        print(f"\nComplete time : {round(duration,2)} sec")



