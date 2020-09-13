import unittest
from hsyapi import HSYAPI

class TestHSYpy(unittest.TestCase):
    def test_parsing(self):
        f = open("sample.html", "r")
        sample_content = f.read()
        f.close()

        api = HSYAPI()

        parsed_data = api.parse(sample_content)
        self.assertEqual(parsed_data[0], 'Muovi - maanantai / Seuraava tyhjennys: 14.9.2020')
        self.assertEqual(parsed_data[1], 'Sekajäte - torstai / Seuraava tyhjennys: 17.9.2020')

if __name__ == "__main__":
    unittest.main()
