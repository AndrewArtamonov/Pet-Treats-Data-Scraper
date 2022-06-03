import re
import time

from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement

# CHANGE SHEET NAME FOR KOHEPETS!!!!
from libraries.common import get_report_file_headers


class KohePets:
    def __init__(self):
        self.dry_food_url = "https://www.kohepets.com.sg/collections/dry-dog-food"
        self.dehydrated_food_url = "https://www.kohepets.com.sg/collections/raw-dehydrated-dog-food"
        self.frozen_food_url = "https://www.kohepets.com.sg/collections/frozen-dog-food"
        self.canned_food_url = "https://www.kohepets.com.sg/collections/canned-dog-food"
        self.tray_food_url = "https://www.kohepets.com.sg/collections/tray-dog-food"
        self.moist_food_url = "https://www.kohepets.com.sg/collections/moist-dog-food"

        self.chromedriver_path = "/Users/andriyartamonov/Documents/chromedriver"
        options = Options()
        # options.headless = True
        options.add_argument("--disable-site-isolation-trials")
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, options=options)

        self.report_file_path = "/Users/andriyartamonov/Documents/PyProj/FreeLance/PetTreats/KohePets.xlsx"
        self.report_file = load_workbook(filename=self.report_file_path, read_only=False)
        self.kohe_pets_sheet = self.report_file["Kohe Pets"]
        self.report_file_headers = get_report_file_headers(self.kohe_pets_sheet)

        self.page = 1
        self.products_processed = 2
        self.nutrition = []

        self.start_time = time.time()

    def process(self):
        # url = ""  #
        # self.process_product("", 2, url)

        self.process_dry_food()

    def process_dry_food(self):
        product_class = "Dry Food"
        product_type = "Dry Food"

        print("*" * 30)
        print("Opening Dry Food main page")
        self.browser.get(url=self.dry_food_url)
        self.browser.maximize_window()

        all_products = self.get_product_elements()
        for idx, product in enumerate(all_products, start=2):
            self.process_product(product, idx, product_class, product_type)

        print(f"Time spended for page - {round((time.time() - self.start_time) / 60, 1)} minutes")
        self.start_time = time.time()

        print("PAGE COMPLETED")
        print("*" * 30)

    def process_product(self, product, row_idx, product_class, product_type, product_url=None):
        product_url: str = product.get_attribute('href') if not product_url else product_url
        print(f"Processing {row_idx - 1} product with url - {product_url}")
        if self.kohe_pets_sheet[f"c{self.products_processed}"].value == product_url:
            print("WAS ALREADY PROCESSED")
            self.products_processed += 1
            return

        self.browser.switch_to.new_window()
        self.browser.get(url=product_url)

        # self.check_and_close_popup()

        product_data_xpath = "//div[@class='col-lg-6 col-md-12 product-intro']"
        product_data_element: WebElement = self.browser.find_element(by=By.XPATH, value=product_data_xpath)

        product_title_xpath = "./h1"
        product_title: str = product_data_element.find_element(by=By.XPATH, value=product_title_xpath).text
        if ': ' in product_title:
            product_title: str = re.findall(pattern=r": (.+)", string=product_title)[0]

        product_image_xpath = "//div[@class='featured-image-wrap d-none d-md-block p-md-4 mb-3 mb-md-0']/img"
        product_image_element = self.browser.find_element(by=By.XPATH, value=product_image_xpath)
        product_image_url = product_image_element.get_attribute("src")

        size_option_xpath = "//ul[@class='variants variants-size']/li/label"
        size_option_elements: list = self.browser.find_elements(by=By.XPATH, value=size_option_xpath)
        sizes_and_prices = {}
        if size_option_elements:
            for idx, option_element in enumerate(size_option_elements, start=1):
                option_text = option_element.text
                size, price = re.findall(pattern=r"(.+).*\n.+\n(.+)", string=option_text)[0]
                if 'Exp' in size:
                    size = re.sub(pattern=r" \(.*", repl="", string=size)
                sizes_and_prices[f"size {idx}"] = size
                sizes_and_prices[f"price {idx}"] = price

        inner_content_xpath = "//div[@class='inner-content']"
        inner_content_text: str = self.browser.find_element(by=By.XPATH, value=inner_content_xpath).text

        # ingredients
        ingredients_pattern = r"/ingredients:?\n([\s\S]+?)\n/gm"
        ingredients_search: list = re.findall(pattern=ingredients_pattern, string=inner_content_text)
        ingredients = ingredients_search[0] if ingredients_search else None

        # proteins, fat, fiber, ash, moisture, calories, phosphorus, calcium, potassium, magnesium
        proteins_search: list = re.findall(pattern=r"protein.*?(\d+\.\d+%)", string=inner_content_text)[0]
        fat_search: list = re.findall(pattern=r"fat .*?(\d+\.\d+%)", string=inner_content_text)[0]
        fiber_search: list = re.findall(pattern=r"(?:fibres|fiber).*?(\d+\.\d+%)", string=inner_content_text)[0]
        ash_search: list = re.findall(pattern=r"ash .*?(\d+\.\d+%)", string=inner_content_text)[0]
        moisture_search: list = re.findall(pattern=r"moisture .*?(\d+\.\d+%)", string=inner_content_text)[0]
        calories_search: list = re.findall(pattern=r"(.*kcal\/kg.*)", string=inner_content_text)[0]
        #  TODO fix calories
        phosphorus_search: list = re.findall(pattern=r"phosphorus .*?(\d+\.\d+%)", string=inner_content_text)[0]
        calcium_search: list = re.findall(pattern=r"calcium .*?(\d+\.\d+%)", string=inner_content_text)[0]
        potassium_search: list = re.findall(pattern=r"potassium .*?(\d+\.\d+%)", string=inner_content_text)[0]
        magnesium_search: list = re.findall(pattern=r"magnesium .*?(\d+\.\d+%)", string=inner_content_text)[0]

        # origin
        origin: list = re.findall(pattern=r"made in (.+)", string=inner_content_text)[0]

        # Ending of product processing
        self.products_processed += 1
        self.report_file.save(filename=self.report_file_path)
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def check_and_close_popup(self):
        close_popup_xpath = "//a[@class='soundest-form-simple-close ']"
        close_popup: list = self.browser.find_elements(by=By.XPATH, value=close_popup_xpath)
        if close_popup:
            close_popup[0].click()

    def get_product_elements(self) -> list:
        self.browser.get(self.dry_food_url)
        self.browser.maximize_window()

        total_products_xpath = "//div[@class='col-md-6 top-toolbar-inner d-none d-md-block']/p"
        total_products_element: WebElement = self.browser.find_element(by=By.XPATH, value=total_products_xpath)
        total_products: str = re.findall(pattern=r"of (\d+) total", string=total_products_element.text)[0]

        product_xpath = "//div[@class='row products-grid main-product-listing']/div[contains(@class, 'col products-grid-item')]//a[@class='title']"
        all_products: list = []

        while int(total_products) != len(all_products):
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            all_products: list = self.browser.find_elements(by=By.XPATH, value=product_xpath)
            time.sleep(2)
        return all_products


if __name__ == "__main__":
    kohe_pets = KohePets()
    kohe_pets.process()
