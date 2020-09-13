import requests
from bs4 import BeautifulSoup
import json

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'

class HSYAPI:
    def __init__(self):
        self.URL = "www.ytvlogistiikka.net/Logica.Ytv.Logistics.Subscription.WebUpdate/fi/Palvelutilaus.aspx/DoLogin/2"
        self.PARAMS = {}
        self.load_creds()

    def load_creds(self):
        with open('cred.json', 'r') as credfile:
            c = json.load(credfile)
    
        assert len(c["palvelutunnus"]) == 13, "Check palvelutunnus in cred.json"
        assert len(c["postinumero"]) == 5, "Check postinumero in cred.json"
        self.PARAMS["HakuehtoPalvelutunnus"] = c["palvelutunnus"]
        self.PARAMS["HakuehtoPostinumero"] = c["postinumero"]

    def update(self):
        r = requests.post("https://" + self.URL, data=self.PARAMS)
        return r

    def parse(self, response):
        result = []
        content = response.split("Tyhjennyspaivat")[1].split("Näytä seuraavat tyhjennyspäivät")[0].split("<table>")[1].split("</table>")[0].split("<tr><td></td></tr>")
        for line in content:
            result.append(BeautifulSoup(line, "lxml").text)
        return result

if __name__ == "__main__":
    api = HSYAPI()
    r = api.update()
    d = api.parse(r.text)
    print(d)
