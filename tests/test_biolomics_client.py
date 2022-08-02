import unittest
from settings import SERVER_URL,TOKEN_URL,CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD,API_VERSION,WEBSITE_ID
from biolomics_client import BiolomicsClient


class TestBiolomicsClient(unittest.TestCase):

    def setUp(self):
        self.client = BiolomicsClient(CLIENT_ID,TOKEN_URL,USERNAME,PASSWORD,
                                      CLIENT_SECRET,SERVER_URL,API_VERSION,WEBSITE_ID)

    def test_get_strain_by_id(self):
        result = "MIRRI0000013"
        js_file_name = self.client.get_strain_by_id(13)
        self.assertEqual(js_file_name,result)


    if __name__ == '__main__':
        unittest.main()