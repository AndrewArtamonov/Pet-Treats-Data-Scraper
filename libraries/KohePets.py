import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class KohePets:
    def __init__(self):
        self.dry_food_url = "https://www.kohepets.com.sg/collections/dry-dog-food"
        self.dehydrated_food_url = "https://www.kohepets.com.sg/collections/raw-dehydrated-dog-food"
        self.frozen_food_url = "https://www.kohepets.com.sg/collections/frozen-dog-food"
        self.canned_food_url = "https://www.kohepets.com.sg/collections/canned-dog-food"
        self.tray_food_url = "https://www.kohepets.com.sg/collections/tray-dog-food"
        self.moist_food_url = "https://www.kohepets.com.sg/collections/moist-dog-food"

        self.chromedriver_path = "/Users/andriyartamonov/Documents/chromedriver"
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path)

        self.all_products_urls = [
            'https://www.kohepets.com.sg/products/instinct-raw-meal-beef-recipe-freeze-dried-dog-food',
            'https://www.kohepets.com.sg/products/eukanuba-puppy-natural-lamb-rice-dry-dog-food',
            'https://www.kohepets.com.sg/products/eukanuba-adult-maintenance-medium-breed-dry-dog-food',
            'https://www.kohepets.com.sg/products/instinct-raw-boost-mixers-blends-freeze-dried-raw-dog-food-topper-5-5oz',
            'https://www.kohepets.com.sg/products/loveabowl-chicken-atlantic-lobster-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/eagle-pro-holistic-life-chicken-for-puppy-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/instinct-limited-ingredient-diet-real-salmon-grain-free-dry-dog-food-4lb',
            'https://www.kohepets.com.sg/products/addiction-mega-grain-free-dry-dog-food-44lb',
            'https://www.kohepets.com.sg/products/eukanuba-puppy-small-breed-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-southwest-canyon-wild-boar-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/nutragold-grain-free-turkey-sweet-potato-dry-dog-food',
            'https://www.kohepets.com.sg/products/nutragold-grain-free-whitefish-sweet-potato-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-viva-la-venison-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-wild-kangaroo-apples-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-zen-vegetarian-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-appalachian-valley-with-venison-small-breed-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-high-prairie-puppy-bison-venison-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-high-prairie-bison-venison-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-pacific-stream-puppy-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-pacific-stream-smoked-salmon-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-pine-forest-with-venison-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-sierra-mountain-roasted-lamb-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/taste-of-the-wild-wetlands-wild-roasted-fowl-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-small-breed-complete-health-turkey-peas-senior-dry-dog-food',
            'https://www.kohepets.com.sg/products/absolute-holistic-duck-peas-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/absolute-holistic-lamb-peas-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/absolute-holistic-pork-peas-lentils-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/absolute-holistic-salmon-peas-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-rawrev-puppy-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-rawrev-small-breed-adult-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-lamb-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-ocean-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-wild-game-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-grain-free-puppy-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-original-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-reduced-fat-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-senior-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-puppy-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-small-breed-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-small-breed-healthy-weight-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-small-breed-puppy-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-rawrev-original-adult-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-chicken-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-duck-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-lamb-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-puppy-chicken-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-whitefish-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-grass-fed-beef-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-salmon-with-pumpkin-quinoa-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-raw-blend-free-range-kibble-with-freeze-dried-raw-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewy-s-raw-blend-red-meat-kibble-with-freeze-dried-raw-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-raw-blend-wild-caught-fish-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-grain-free-adult-deboned-chicken-chicken-meal-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-grain-free-adult-lamb-lamb-meal-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-grain-free-adult-whitefish-menhaden-meal-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-simple-solutions-grain-free-salmon-potato-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-simple-solutions-lamb-oatmeal-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-lamb-barley-salmon-meal-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-puppy-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-complete-health-fish-sweet-potato-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-rawrev-ocean-adult-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-large-breed-formula-dry-dog-food-24lb',
            'https://www.kohepets.com.sg/products/wellness-core-grain-free-large-breed-puppy-formula-dry-dog-food-24lb',
            'https://www.kohepets.com.sg/products/wellness-simple-solutions-grain-free-turkey-potato-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-wild-islands-forest-meat-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-wild-islands-highland-meat-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-wild-islands-island-birds-dry-dog-food',
            'https://www.kohepets.com.sg/products/addiction-wild-islands-pacific-catch-dry-dog-food',
            'https://www.kohepets.com.sg/products/earthmade-free-range-grass-fed-beef-grain-free-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/earthmade-free-range-grass-fed-lamb-grain-free-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/earthmade-new-zealand-mackerel-grain-free-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/bixbi-rawbble-pork-limited-ingredient-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/bixbi-liberty-beef-limited-ingredient-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/bixbi-liberty-fishermans-catch-trout-fish-limited-ingredient-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/bixbi-liberty-original-turkey-chicken-fish-limited-ingredient-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/bixbi-liberty-rancher-s-red-beef-lamb-goat-limited-ingredient-ancient-grain-dry-dog-food',
            'https://www.kohepets.com.sg/products/celtic-connection-chicken-with-turkey-sweet-potato-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/celtic-connection-lamb-with-goat-sweet-potato-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/celtic-connection-salmon-with-trout-sweet-potato-grain-free-dry-dog-food',
            'https://www.kohepets.com.sg/products/stella-chewys-freeze-dried-raw-coated-kibble-small-breed-chicken-dry-dog-food-3-5lb',
            'https://www.kohepets.com.sg/products/stella-chewys-small-breed-raw-blend-red-meat-kibble-with-freeze-dried-raw-grain-free-dry-dog-food-3-5lb',
            'https://www.kohepets.com.sg/products/simple-food-project-chicken-turkey-freeze-dried-raw-dog-food',
            'https://www.kohepets.com.sg/products/wellness-core-digestive-health-chicken-brown-rice-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/anf-chicken-meal-rice-adult-dry-dog-food',
            'https://www.kohepets.com.sg/products/anf-holistic-lamb-brown-rice-dry-dog-food',
            'https://www.kohepets.com.sg/products/anf-holistic-fish-meal-potato-dry-dog-food',
            'https://www.kohepets.com.sg/products/anf-holistic-senior-lamb-rice-dry-dog-food',
            'https://www.kohepets.com.sg/products/bow-wow-origi-7-lamb-air-dried-soft-dry-dog-food-1-2kg',
            'https://www.kohepets.com.sg/products/bow-wow-zenith-grain-free-soft-kibble-light-senior-dry-dog-food-1-2kg',
            'https://www.kohepets.com.sg/products/bow-wow-zenith-grain-free-soft-kibble-small-breed-dry-dog-food-1-2kg',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-australian-lamb-formula-small-bites-dry-dog-food',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-chicken-meal-with-blueberries-formula-small-bites-dry-dog-food',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-pacific-ocean-fish-puppy-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-pacific-ocean-fish-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-pacific-ocean-fish-formula-small-bites-dry-dog-food',
            'https://www.kohepets.com.sg/products/bow-wow-zenith-grain-free-soft-kibble-puppy-dry-dog-food-1-2kg',
            'https://www.kohepets.com.sg/products/firstmate-grain-free-pacific-ocean-fish-weight-control-formula-dry-dog-food',
            'https://www.kohepets.com.sg/products/golden-eagle-holistic-health-chicken-formula-26-15-dry-dog-food',
            'https://www.kohepets.com.sg/products/golden-eagle-holistic-health-duck-with-oatmeal-dry-dog-food']
        self.processed_urls = ['https://www.kohepets.com.sg/products/instinct-raw-meal-beef-recipe-freeze-dried-dog-food',]

    def process(self):
        self.process_dry_food()

    def process_dry_food(self):
        all_products = self.get_product_elements()

        for product in all_products:
        # for product in self.all_products_urls:
            product_link = product.get_attribute('href')
            # self.browser.get(url=product_link)

            # if product in self.processed_urls:
            #     continue

            self.browser.get(url=product)
            self.check_and_close_popup()

            product_data_xpath = "//div[@class='col-lg-6 col-md-12 product-intro']"
            product_data_element: WebElement = self.browser.find_element(by=By.XPATH, value=product_data_xpath)

            product_title_xpath = "./h1"
            product_title: str = product_data_element.find_element(by=By.XPATH, value=product_title_xpath).text

            if ': ' in product_title:
                title: str = re.findall(pattern=r": (.+)", string=product_title)[0]
            # url = product_link
            url = product

            product_image_xpath = "//div[@class='featured-image-wrap d-none d-md-block p-md-4 mb-3 mb-md-0']/img"
            product_image_element = self.browser.find_element(by=By.XPATH, value=product_image_xpath)
            product_image_url = product_image_element.get_attribute("src")

            product_type = product_class = "Dry Food"

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


            print()

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
