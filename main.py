from prepareStrains import prepare_strains
from createDataset import publish_dataset
import time
import sys



def set_singl_dataset(record_ID):
    json_file_name = prepare_strains(record_ID)
    if json_file_name == False:
        sys.exit("Oups !")
    else:
        publish_dataset(json_file_name)


def set_multi_dataset(record_ID,record_ID_max):

    while record_ID <= record_ID_max :
        print(f"\nExecuting: record {record_ID}")
        json_file_name = prepare_strains(record_ID)
        publish_dataset(json_file_name)
        record_ID += 1



if __name__ == '__main__':
    begin = time.time()
    #set_multi_dataset(45,54)
    set_singl_dataset(9879)
    end = time.time()
    duration = end  - begin
    print(f"\nComplete time : {duration} seconds")



