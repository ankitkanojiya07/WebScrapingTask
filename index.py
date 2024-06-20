import requests
from lxml import html
from PIL import Image
import json
from io import BytesIO

class TINXSYSWebScraper:
    def __init__(self, tin_number):
        self.url = "https://tinxsys.com/TinxsysInternetWeb/searchByTin_Inter.jsp"
        self.tin_number = tin_number
        self.session = requests.Session()

    def fetch_captcha(self):
        response = self.session.get(self.url)
        tree = html.fromstring(response.content)
        captcha_image_url = tree.xpath('//img[@id="captchaImg"]/@src')[0]
        captcha_image_response = self.session.get(captcha_image_url)
        img = Image.open(BytesIO(captcha_image_response.content))
        img.show()
        captcha_text = input("Enter CAPTCHA: ")
        return captcha_text

    def get_data(self):
        captcha_text = self.fetch_captcha()
        payload = {
            'tinNumber': self.tin_number,
            'captchaText': captcha_text
        }
        response = self.session.post(self.url, data=payload)
        tree = html.fromstring(response.content)
        
        data = {
            'tin_number': self.tin_number,
            'cst_number': self.extract_data(tree, '//span[@id="cstNumber"]/text()'),
            'dealer_name': self.extract_data(tree, '//span[@id="dealerName"]/text()'),
            'dealer_address': self.extract_data(tree, '//span[@id="dealerAddress"]/text()'),
            'state_name': self.extract_data(tree, '//span[@id="stateName"]/text()'),
            'pan_number': self.extract_data(tree, '//span[@id="panNumber"]/text()'),
            'registration_date': self.extract_data(tree, '//span[@id="registrationDate"]/text()'),
            'valid_upto': self.extract_data(tree, '//span[@id="validUpto"]/text()'),
            'registration_status': self.extract_data(tree, '//span[@id="registrationStatus"]/text()')
        }
        return data

    def extract_data(self, tree, xpath_expr):
        result = tree.xpath(xpath_expr)
        return result[0].strip() if result else None

    def save_to_json(self, data, filename='data.json'):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    tin_number = "21711100073"
    scraper = TINXSYSWebScraper(tin_number)
    data = scraper.get_data()
    print(json.dumps(data, indent=4))
    scraper.save_to_json(data)
