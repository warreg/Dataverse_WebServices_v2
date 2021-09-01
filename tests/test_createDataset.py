import unittest
import createDataset
import re

class TestCreateDataset(unittest.TestCase):

    def test_create_dataset(self):
        doi = createDataset.create_dataset("MIRRI0000013")
        # pattern_exp: doi:10.21386/FK2/C6VMUM
        result = re.search("^doi:\d+\.\d+\/.+",doi)
        self.assertTrue(result)


    def test_upload_file(self):
        persistent_ID = createDataset.upload_file("MIRRI0000013")
        result = re.search("^doi:\d+\.\d+\/.+",persistent_ID)
        self.assertTrue(result)


    def test_publish_dataset(self):
        func_return = createDataset.publish_dataset("MIRRI0000013")
        result = "OK"
        self.assertEqual(func_return,result)



    if __name__ == '__main__':
        unittest.main()