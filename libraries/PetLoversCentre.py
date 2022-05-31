import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class PetLovers:
    def __init__(self):
        self.dry_food_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/dry-food"
        self.food_pouches_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/food-pouches"
        self.canned_food_url = "https://www.petloverscentre.com/dog/dog-food-treats/food/canned-food"
        self.broth_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/broth"
        self.air_dried_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/air-dried"
        self.dehydrated_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/dehydrated"
        self.freeze_dried_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/freeze-dried"
        self.frozen_url = "https://www.petloverscentre.com/dog/dog-food-treats/dog-dog-food-treats-food/frozen-food"

        self.chromedriver_path = "/Users/andriyartamonov/Documents/chromedriver"
        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path)

    def process(self):
        self.process_dry_food()

    def process_dry_food(self):
        self.browser.get(url=self.dry_food_url)
