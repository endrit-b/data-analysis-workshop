from bs4 import BeautifulSoup
import requests
from pprint import pprint
import sys
import csv


class ManufacturerScraper:

    def __init__(self):
        self.TARGET_BASE_URL = 'https://www.urparts.com/'
        self.CATALOG_URL = 'https://www.urparts.com/index.cfm/page/catalogue'
        self.csv_header = ['manufacturer', 'category', 'model', 'part', 'part_category']
        self.OUTPUT_PATH = '../data/output'

    def scrape(self, maker_filter=None):
        """
        A method that will scrape all manufacturer parts and relevant info from catalog
        :param maker_filter: If a filter is given, we'll scrape only data for that manufacturer
        :return: <void> - a CSV file write will be generated
        """
        # Get manufacturers from catalog
        makers = self.scrape_data_from_manufactures_catalog('c_container allmakes', self.CATALOG_URL)

        # Check if given manufacturer is valid
        if maker_filter is not None:
            if not (maker_filter in makers):
                raise Exception(f'No manufacturer {maker_filter} found!')
            else:
                makers = [maker_filter]

        # For demo purposes I'm limiting the scraping to only first maker
        for maker in makers[:1]:
            file = open(f'{self.OUTPUT_PATH}/{maker.lower().replace(" ", "")}_maker.csv', 'w+')
            writer = csv.writer(file)
            writer.writerow(self.csv_header)
            # Get categories
            categories = self.scrape_data_from_manufactures_catalog('c_container allmakes allcategories',
                                                                    self.CATALOG_URL + '/' + maker)
            for category in categories:
                # Get models
                models = self.scrape_data_from_manufactures_catalog('c_container allmodels',
                                                                    self.CATALOG_URL + '/' + maker + '/' + category)
                for model in models:
                    row = [maker, category, model]
                    print(f'** Scraping "{",".join(row)}"')
                    # Get parts
                    parts = self.scrape_data_from_manufactures_catalog('c_container allparts',
                                                                       self.CATALOG_URL + '/' + maker + '/' + category + '/' + model)
                    # Flatten and prepare row structure
                    rows = list(map(lambda part: row + list(map(str.strip, part.split('-'))), parts))
                    # Write to file
                    writer.writerows(rows)

            # Close file stream
            file.close()

    @staticmethod
    def scrape_data_from_manufactures_catalog(html_tag_cls, link_url):
        """
        A method to scrape the manufacturers data from the catalog
        :param html_tag_cls:
        :param link_url:
        :return:
        """
        html_doc = requests.get(link_url).text
        landing_pg = BeautifulSoup(html_doc, 'html.parser')
        makers_div = landing_pg.find('div', class_=html_tag_cls)
        data = []
        # Get list of makers from list HTML tag
        for maker in makers_div.find_all('li'):
            link = maker.find("a")
            data.append(link.text.strip())
        return data
