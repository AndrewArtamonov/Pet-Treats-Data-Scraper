import re
import time

from openpyxl import load_workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
        options = Options()
        options.headless = True
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, options=options)
        # self.browser = webdriver.Chrome(executable_path=self.chromedriver_path)

        self.report_file_path = "Scraping Masterlist.xlsx"
        self.report_file = load_workbook(filename=self.report_file_path, read_only=False)
        self.pet_lovers_sheet = self.report_file["Pet Lovers Centre"]
        self.report_file_headers = self.get_report_file_headers()

        self.page = 1
        self.products_processed = 2
        self.nutrition = []

    def process(self):
        # url = "https://www.petloverscentre.com/products/figlicious-venison-feast-grain-free-2lbs" #min value
        # self.process_product("", 2, url)

        self.process_dry_food()

    def process_dry_food(self):
        print("Opening Dry Food main page")
        self.browser.get(url=self.dry_food_url)
        self.browser.maximize_window()

        last_page = False
        for _ in range(2):
            print(f"Processing {self.page} page")
            product_xpath = "//div[@class='product-box col-1-3 tab-col-1-2 mobile-col-1-1']/div[@class='prod-img']//a"
            page_products_links: list = self.browser.find_elements(by=By.XPATH, value=product_xpath)

            for idx, product in enumerate(page_products_links, start=2):
                self.process_product(product, idx)

            next_page_button_xpath = "//div[@class='page-no-top col-2-3']/ul[@class='page-prev-next']"
            button_element = self.browser.find_element(by=By.XPATH, value=next_page_button_xpath)
            button_size = button_element.size['height']
            if button_size:
                self.page += 1
                button_element.click()
            else:
                print("ALL PAGES COMPLETED")
                return

    def process_product(self, product, row_idx, product_url=None):
        product_url: str = product.get_attribute('href') if not product_url else product_url
        print(f"Processing {row_idx - 1} product with url - {product_url}")
        product_class = "Dry Food"
        product_type = "Dry Food"

        self.browser.switch_to.new_window()
        self.browser.get(url=product_url)

        brand_name_xpath = "//p[@class='small-name']"
        brand_name: str = self.browser.find_element(by=By.XPATH, value=brand_name_xpath).text

        title_xpath = "//div[@class='prod-details-top col-1-1']/h1"
        title_text: str = self.browser.find_element(by=By.XPATH, value=title_xpath).text
        product_size = ""
        product_size_in_title = re.findall(r" (\d+(?:\.\d+)?(?:g|kg|lbs))$", title_text, re.IGNORECASE)
        if product_size_in_title:
            product_size = product_size_in_title[0]
            product_title = title_text.replace(product_size, "").strip()
            product_title: str = brand_name + " - " + product_title
        elif "lbs" in title_text and "kg" in title_text:
            regexp_size_pattern = re.compile(r" \d+(?:\.\d+)?lbs \((\d+(?:\.\d+)?kg)\)")
            product_size = re.findall(pattern=regexp_size_pattern, string=title_text)[0]
            product_title = brand_name + " - " + re.sub(pattern=regexp_size_pattern, repl="", string=title_text)
        else:
            product_title: str = brand_name + " - " + title_text

        product_image_url: str = self.get_product_image_url()

        price_xpath = "//div[@class='prod-price']/p[1]"
        product_price: str = self.browser.find_element(by=By.XPATH, value=price_xpath).text

        product_details_xpath = "//div[@id='details']"
        product_details_text: str = self.browser.find_element(by=By.XPATH, value=product_details_xpath).text

        product_size: str = self.get_product_size(product_details_text,
                                                  title_text) if not product_size else product_size

        product_nutrition_table_xpath = "(//div[@id='details']//table)[1]//tr"
        product_nutrition_table = self.browser.find_elements(by=By.XPATH, value=product_nutrition_table_xpath)
        product_elements = {}
        for element in product_nutrition_table:
            name_value_separator_xpath = "./td"
            name, value = element.find_elements(by=By.XPATH, value=name_value_separator_xpath)

            name = self.process_nutrition_name(name)
            value = self.process_nutrition_value(value)

            product_elements[name] = value
        if len(product_elements.keys()) != len(product_nutrition_table):
            print("ERROR DURING NUTRITION PARSING")
        product_origin: str = re.findall(pattern=r"Made in (.+)", string=product_details_text)[0]

        product_ingredients_regexp = r"Ingredients:\n([\s\S]+?)(?:Analysis|Made in)"
        product_ingredients: str = re.findall(pattern=product_ingredients_regexp, string=product_details_text)[0]
        product_ingredients = product_ingredients.replace("\n", "").replace(".SUPPLEMENTS:", ",").replace(
            ".Supplements:", "")

        product_data = ["Pet Lovers Centre", product_title, product_url, product_image_url, product_type, product_class,
                        product_size, product_price, product_origin, product_ingredients]

        for column_idx, value in enumerate(product_data, start=1):
            self.pet_lovers_sheet.cell(self.products_processed, column_idx, value)

        for key, value in product_elements.items():
            if key not in self.report_file_headers:
                new_header_index = len(self.report_file_headers) + 1
                self.pet_lovers_sheet.cell(1, new_header_index, key)
                self.pet_lovers_sheet.cell(row_idx, new_header_index, value)
                self.report_file_headers.append(key)

                self.nutrition.append(key)
            else:
                column_idx = self.report_file_headers.index(key) + 1
                self.pet_lovers_sheet.cell(row_idx, column_idx, value)

        self.products_processed += 1
        self.report_file.save(filename=self.report_file_path)
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])

    def get_product_image_url(self):
        image_div_xpath = "//div[@class='zoomContainer']/div/div"
        image_div_element: WebElement = self.browser.find_element(by=By.XPATH, value=image_div_xpath)
        image_div_style: str = image_div_element.get_attribute("style")
        product_image_url: str = re.findall(pattern=r'url\("(.+)"\)', string=image_div_style)[0]
        return product_image_url

    def get_product_size(self, product_details_text: str, title_text: str):
        product_size_from_title = re.findall(pattern=r"(\d+(?:\.\d+)? ?kg)", string=title_text)
        product_size = product_size_from_title[0] if product_size_from_title else ""
        if not product_size:
            product_size_from_description: list = re.findall(pattern=r"Size:\n(.+)", string=product_details_text)
            product_size = product_size_from_description[0] if product_size_from_description else ""
        product_size = product_size.strip().replace(" ", "")
        return product_size

    @staticmethod
    def process_nutrition_name(name: WebElement) -> str:
        name = name.text.strip()
        name = "Glucosamine" if "glucosamine" in name.lower() else name
        name = "Chondroitin" if "chondroitin" in name.lower() else name
        name = "Phosphorus" if "phosphorus" in name.lower() else name
        name = "Crude Ash" if "ash" in name.lower() else name
        name = "Crude Protein" if "protein" in name.lower() else name
        name = "Crude Fat" if "fat" in name.lower() and not re.findall(pattern=r"fat\w+", string=name,
                                                                       flags=re.IGNORECASE) else name
        name = "Crude Fiber" if "fiber" in name.lower() or "fibres" in name.lower() else name
        name = "DHA" if "dha" in name.lower() else name
        name = "EPA" if "epa" in name.lower() else name
        name = "NFE" if "nfe" in name.lower() else name
        name = "ME" if "me" in name.lower() else name
        name = "Calories" if "calori" in name.lower() else name
        name = "Linoleic Acid" if "linoleic acid" in name.lower() else name
        name = "Omega-3" if re.findall(pattern=r"omega[-‑ ]3", string=name, flags=re.IGNORECASE) else name
        name = "Omega-6" if re.findall(pattern=r"omega[-‑ ]6", string=name, flags=re.IGNORECASE) else name
        name = "Omega-7" if re.findall(pattern=r"omega[-‑ ]7", string=name, flags=re.IGNORECASE) else name
        name = "Omega-9" if re.findall(pattern=r"omega[-‑ ]9", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin A" if re.findall(pattern=r"vitamin\.? a(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin B1" if re.findall(pattern=r"vitamin\.? b1(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin B2" if re.findall(pattern=r"vitamin\.? b2(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin B3" if re.findall(pattern=r"vitamin\.? b3(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin B5" if re.findall(pattern=r"vitamin\.? b5(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin B6" if re.findall(pattern=r"vitamin\.? b6(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin D3" if re.findall(pattern=r"vitamin\.? d3(?:$| )", string=name, flags=re.IGNORECASE) else name
        name = "Vitamin E" if re.findall(pattern=r"vitamin\.? e(?:$| )", string=name, flags=re.IGNORECASE) else name
        return name

    @staticmethod
    def process_nutrition_value(value: WebElement) -> str:
        if "min" in value.text.lower() and "max" in value.text.lower():
            value = re.sub(pattern=r"min.+,", repl="", string=value.text, flags=re.IGNORECASE)
        else:
            value = value.text
        value = value.replace("Min.", "").replace("Max.", "")
        value = value.replace("min.", "").replace("max.", "")
        value = value.replace("Min", "").replace("Max", "")
        value = value.replace("min", "").replace("max", "").replace("()", "").replace("-", "")
        if 'IU/kg' in value:
            value = re.sub(r"(\d) (\d)", r"\1\2", value)
            value = value.replace(",", "")
        elif "%" in value:
            value = value.replace(" ", "")
        value = re.sub(r"\.00%", ".0%", value)
        value = value.strip()
        return value

    def get_report_file_headers(self) -> list:
        first_row: list = list(self.pet_lovers_sheet)[0]
        headers: list = [cell.value for cell in first_row if cell.value]
        return headers
