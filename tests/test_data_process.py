import unittest
from data_process import get_data_values,update_template


class TestDataProcess(unittest.TestCase):

    def test_get_data_values(self):
        result = {"ds_title":"Chryseobacterium mulctrae",
                  "ds_author_name":"BEA",
                  "ds_author_affiliation":"BEA",
                  "ds_contact_email":"v.robert@cbs.knaw.nl",
                  "ds_contact_name":"BEA",
                  "ds_description":"for commercial development a special agreement is requested"}

        data_values = get_data_values("MIRRI0000013")
        self.assertEqual(data_values,result)


    def test_update_template(self):
        data_val = {"ds_title":"Chryseobacterium mulctrae",
                  "ds_author_name":"BEA",
                  "ds_author_affiliation":"BEA",
                  "ds_contact_email":"v.robert@cbs.knaw.nl",
                  "ds_contact_name":"BEA",
                  "ds_description":"for commercial development a special agreement is requested"}

        template_dict = update_template(data_val)
        result_title = template_dict["datasetVersion"]["metadataBlocks"]["citation"]["fields"][0]["value"]

        self.assertEqual("Chryseobacterium mulctrae",result_title)

    def test_set_metadata_file(self):
        pass


    if __name__ == '__main__':
        unittest.main()