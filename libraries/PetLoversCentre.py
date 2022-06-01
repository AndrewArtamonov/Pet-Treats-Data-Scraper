import re
import time

from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PetLovers:
    def __init__(self):
        self.dry_food_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/dry-food?SortBy=Brand&SortOrder=Asc"
        self.food_pouches_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/food-pouches"
        self.canned_food_url = "https://www.petloverscentre.com/dog/dog-food-treats/food/canned-food"
        self.broth_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/broth"
        self.air_dried_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/air-dried"
        self.dehydrated_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/dehydrated"
        self.freeze_dried_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/freeze-dried"
        self.frozen_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/frozen-food"

        self.chromedriver_path = "/Users/andriyartamonov/Documents/chromedriver"
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path)

        self.report_file_path = "Scraping Masterlist.xlsx"
        self.report_file = load_workbook(filename=self.report_file_path, read_only=False)
        self.pet_lovers_sheet = self.report_file["Pet Lovers Centre"]
        self.report_file_headers = self.get_report_file_headers()

    def process(self):
        self.process_dry_food()

    def process_dry_food(self):
        self.browser.get(url=self.dry_food_url)
        self.browser.maximize_window()

        product_xpath = "//div[@class='product-box col-1-3 tab-col-1-2 mobile-col-1-1']/div[@class='prod-img']//a"
        page_products_links: list = self.browser.find_elements(by=By.XPATH, value=product_xpath)

        for idx, product in enumerate(page_products_links, start=2):
            self.process_product(product, idx)
        print()

    def process_product(self, product, row_idx):
        product_url: str = product.get_attribute('href')
        product_class = "Dry Food"
        product_type = "Dry Food"

        self.browser.switch_to.new_window()
        self.browser.get(url=product_url)

        brand_name_xpath = "//p[@class='small-name']"
        brand_name: str = self.browser.find_element(by=By.XPATH, value=brand_name_xpath).text

        title_xpath = "//div[@class='prod-details-top col-1-1']/h1"
        title_text: str = self.browser.find_element(by=By.XPATH, value=title_xpath).text
        product_title: str = re.sub(pattern=r",? \d+(?:\.\d+)? ?kg", repl="", string=title_text)
        product_title: str = brand_name + " - " + product_title

        image_div_xpath = "//div[@class='zoomContainer']/div/div"
        image_div_element: WebElement = self.browser.find_element(by=By.XPATH, value=image_div_xpath)
        image_div_style: str = image_div_element.get_attribute("style")
        product_image_url: str = re.findall(pattern=r'url\("(.+)"\)', string=image_div_style)[0]

        price_xpath = "//div[@class='prod-price']/p[1]"
        product_price: str = self.browser.find_element(by=By.XPATH, value=price_xpath).text

        product_details_xpath = "//div[@id='details']"
        product_details_text: str = self.browser.find_element(by=By.XPATH, value=product_details_xpath).text

        product_size: list = re.findall(pattern=r"Size:\n(.+)", string=product_details_text)
        product_size = product_size[0] if product_size else ""

        product_nutrition_table_xpath = "//b[contains(text(), 'Analysis')]/ancestor::div[1]/following-sibling::div[1]//tr"
        product_nutrition_table = self.browser.find_elements(by=By.XPATH, value=product_nutrition_table_xpath)
        product_elements = {}
        for element in product_nutrition_table:
            name_value_separator_xpath = "./td"
            name, value = element.find_elements(by=By.XPATH, value=name_value_separator_xpath)

            name = name.text
            name = "Glucosamine" if "Glucosamine" in name else name
            name = "Chondroitin" if "Chondroitin" in name else name
            value = value.text.replace("Min. ", "").replace("Max. ", "").strip()

            product_elements[name] = value

        product_origin: str = re.findall(pattern=r"Made in (.+)", string=product_details_text)[0]

        product_ingredients: str = re.findall(pattern=r"Ingredients:\n(.+).", string=product_details_text)[0]

        product_data = ["Pet Lovers Centre", product_title, product_url, product_image_url, product_type, product_class,
                        product_size, product_price, product_origin, product_ingredients]

        for column_idx, value in enumerate(product_data, start=1):
            self.pet_lovers_sheet.cell(row_idx, column_idx, value)

        for key, value in product_elements.items():
            if key not in self.report_file_headers:
                new_header_index = len(self.report_file_headers) + 1
                self.pet_lovers_sheet.cell(1, new_header_index, key)
                self.pet_lovers_sheet.cell(row_idx, new_header_index, value)
                self.report_file_headers.append(key)
            else:
                column_idx = self.report_file_headers.index(key) + 1
                self.pet_lovers_sheet.cell(row_idx, column_idx, value)

        self.report_file.save(filename=self.report_file_path)

        print("Finished product processing")

        self.browser.close()
        browser_windows = self.browser.window_handles
        self.browser.switch_to.window(browser_windows[0])

        print()

    def get_report_file_headers(self) -> list:
        first_row: list = list(self.pet_lovers_sheet)[0]
        headers: list = [cell.value for cell in first_row if cell.value]
        return headers
