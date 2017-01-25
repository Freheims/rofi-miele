import requests
from lxml import etree
from rofi import Rofi

class RofiMiele:
    def __init__(self):
        self.rofi = Rofi()
        self.api_auth = ("username", "password")
        self.api_endpoint = "LaundryState"

    def fetchLaundry(self, address):
        url = "{}/{}".format(address, self.api_endpoint)
        response = requests.get(url, auth=self.api_auth)
        if response.status_code == 200:
            return response.text
        else:
            return False

    def getLaundry(self, code):
        machines = []
        addr = ""
        if code == 0:
            addr = "http://84.214.150.62"
        elif code == 1:
            addr = "http://84.214.150.66"

        html = self.fetchLaundry(addr)
        if not html:
            self.rofi.error("Kunne ikkje laste info :(")
            sys.exit(1)

        root = etree.HTML(html)
        res = root.xpath(".//td[@class='p']")
        for i in res:
            machine = i.getchildren()
            status = " ".join([tags.tail for tags in machine[0:] if tags.tail])
            machines.append(machine[0].text + " " + status)
        return machines

    def run(self):
        laundries = ["52","54"]
        index, status = self.rofi.select("Vaskeri: ", laundries)
        laundry = self.getLaundry(index)
        self.rofi.select("Vaskeri " + laundries[index], laundry)

rofi_miele = RofiMiele()
rofi_miele.run()
