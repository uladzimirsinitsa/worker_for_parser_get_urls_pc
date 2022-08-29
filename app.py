
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from flask import Flask
from flask import request

from bs4 import BeautifulSoup

app = Flask(__name__)


def check_url(url):
    return 'pulscen.ru' in url


@app.route('/', methods=['GET'])
def parser():
    urls = []
    if request.args['url']:
        url = request.args['url']
        for url in [url]:
            service = Service(executable_path=r'/usr/src/app/chromedriver')
            options = ChromeOptions()
            options.headless = True
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url)

            soup = BeautifulSoup(driver.page_source, 'lxml')
            if soup.find(class_='fs13 mt20'):
                return {'response': 'fs13 mt20.Im ready for the next task.'}
            try:
                data = soup.find(id='products-list').find_all(class_='product-listing__item')
            except AttributeError:
                continue
            for item in data:
                try:
                    url = item.find(class_='product-listing__product-info-wrapper').find('a').get('href')
                    urls.append(url)
                except AttributeError:
                    continue
            driver.quit()
            return {'urls': urls}


if __name__ == "__main__":
    app.run(debug=False)
