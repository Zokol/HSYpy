import requests
from bs4 import BeautifulSoup
import json
import datetime

"""
Select allowed cipher
"""
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

class HSYAPI:
    """
    Initialize API

    self.URL: API URL
    self.PARAMS: Parameters for connecting HSY API
    """
    def __init__(self):
        self.URL = "www.ytvlogistiikka.net/Logica.Ytv.Logistics.Subscription.WebUpdate/fi/Palvelutilaus.aspx/DoLogin/2"
        self.PARAMS = {}
        self.load_creds()

    """
    Load creds

    Reads creds.json-file for login credentials
    """
    def load_creds(self):
        with open('cred.json', 'r') as credfile:
            c = json.load(credfile)
    
        assert len(c["palvelutunnus"]) == 13, "Check palvelutunnus in cred.json"
        assert len(c["postinumero"]) == 5, "Check postinumero in cred.json"
        self.PARAMS["HakuehtoPalvelutunnus"] = c["palvelutunnus"]
        self.PARAMS["HakuehtoPostinumero"] = c["postinumero"]

    """
    Update

    Reads raw response of POST-request from API
    """
    def update(self):
        r = requests.post("https://" + self.URL, data=self.PARAMS)
        return r

    """
    Parse

    Extract the interesting information out of the HTML-response

    Returns dict in format: {waste_type: dates_until_collected}
    Example: {"Mixed": -1, "Plastic": -3}
    """
    def parse(self, response):
        parsed = []
        result = {}
        content = response.split("Tyhjennyspaivat")[1].split("Näytä seuraavat tyhjennyspäivät")[0].split("<table>")[1].split("</table>")[0].split("<tr><td></td></tr>")
        for line in content:
            parsed.append(BeautifulSoup(line, "lxml").text)
        for line in parsed:
            try:
                if len(line) == 0: continue
                t = line.split(" ")  ## Split line into words.
                waste_type = t[0]   ## Extract waste type (first word in line)
                collection_date = datetime.datetime.strptime(t[-1], '%d.%m.%Y')  ## Convert string to datetime
                collection_delta = (collection_date - datetime.datetime.now()).days  ## Calculate delta of now and collection date
                result[waste_type] = collection_delta   ## Store result
            except Exception:
                continue
        return result

if __name__ == "__main__":
    api = HSYAPI()
    r = api.update()
    d = api.parse(r.text)
    print(d)
