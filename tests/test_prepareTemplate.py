import unittest
from prepareTemplate import update_dv_template

class TestPrepareTemplate(unittest.TestCase):

    def test_update_dv_template(self):
        result = "MIRRI0000013"
        json_file_name = update_dv_template(13)
        self.assertEqual(json_file_name,result)


    if __name__ == '__main__':
        unittest.main()