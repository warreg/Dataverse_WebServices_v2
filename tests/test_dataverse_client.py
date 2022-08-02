import unittest
from settings import DATAVERSE_SERVER,API_TOKEN,PARENT,MAJOR_OR_MINOR
from dataverse_client import DataverseClient
import re

class TestDataverseClient(unittest.TestCase):

    def setUp(self):
        self.client = DataverseClient(DATAVERSE_SERVER,API_TOKEN,PARENT,MAJOR_OR_MINOR)

    def test_create_dataset(self):
        doi = self.client.create_dataset("MIRRI0000013")
        # pattern_exp: doi:10.21386/FK2/C6VMUM
        pattern = "^doi:\d+\.\d+\/.+"
        result = re.search(pattern,doi)
        self.assertTrue(result)


    def test_upload_file(self):
        persistent_ID = self.client.upload_file("MIRRI0000013","doi:10.21386/FK2/C6VMUM")
        pattern = "^doi:\d+\.\d+\/.+"
        result = re.search(pattern,persistent_ID)
        self.assertTrue(result)


    def test_publish_dataset(self):
        pass
        # published = self.client.publish_dataset("doi:10.21386/FK2/OIGE2S")
        # self.assertTrue(published)




    if __name__ == '__main__':
        # unittest.main()
        test_create_dataset()