import unittest
from getStrains import get_strain_by_id

class TestGetStrains(unittest.TestCase):

    def test_get_strain_by_id(self):
        result = "MIRRI0000013"
        json_file_name = get_strain_by_id(13)
        self.assertEqual(json_file_name,result)


    if __name__ == '__main__':
        unittest.main()