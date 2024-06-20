import requests
from lxml import html
from PIL import Image
from io import BytesIO
import json

class TinxsysScraper:
    def __init__(self, tin_number):
        self.base_url = "https://tinxsys.com/TinxsysInternetWeb/searchByTin_Inter.jsp"
        self.tin_number = tin_number
        self.session = requests.Session()
    
    def get_captcha(self):
        response = self.session.get(self.base_url)
        tree = html.fromstring(response.content)
        captcha_url = tree.xpath('//img[@id="captchaImg"]/@src')[0]
        captcha_response = self.session.get(f'https://tinxsys.com{captcha_url}', stream=True)
        img = Image.open(BytesIO(captcha_response.content))
        img.show()
        captcha = input("Please enter CAPTCHA: ")
        return captcha
    
    def scrape(self):
        captcha = self.get_captcha()
        payload = {
            'tinNumber': self.tin_number,
            'captcha': captcha
        }
        response = self.session.post(self.base_url, data=payload)
        tree = html.fromstring(response.content)
        return self.parse_data(tree)
    
    def parse_data(self, tree):
        data = {
            'tin_number': self.tin_number,
            'cst_number': self.extract_text(tree, '//span[@id="cstNumberId"]/text()'),
            'dealer_name': self.extract_text(tree, '//span[@id="dealerNameId"]/text()'),
            'dealer_address': self.extract_text(tree, '//span[@id="dealerAddressId"]/text()'),
            'state_name': self.extract_text(tree, '//span[@id="stateNameId"]/text()'),
            'pan_number': self.extract_text(tree, '//span[@id="panNumberId"]/text()'),
            'registration_date': self.extract_text(tree, '//span[@id="dateOfRegId"]/text()'),
            'valid_upto': self.extract_text(tree, '//span[@id="validUptoId"]/text()'),
            'registration_status': self.extract_text(tree, '//span[@id="regStatusId"]/text()'),
        }
        return data
    
    def extract_text(self, tree, xpath):
        result = tree.xpath(xpath)
        return result[0].strip() if result else None

    def to_json(self, data):
        return json.dumps(data, indent=4)

if __name__ == "__main__":
    tin_number = "09137500718"
    scraper = TinxsysScraper(tin_number)
    data = scraper.scrape()
    print(scraper.to_json(data))
