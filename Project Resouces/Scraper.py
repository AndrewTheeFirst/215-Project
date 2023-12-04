#Andrew Patton
#Christopher Pillgreen

# from bs4 import BeautifulSoup
# import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

class Amazon:

    def __init__(self, isbn):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(3)
        self.search(isbn)
        things = self.parse()
        print(things)

    def search(self, isbn: int) -> None:
        link = f'https://www.amazon.com/s?i=stripbooks&rh=p_66%3A\
            {isbn}&s=relevanceexprank&Adv-Srch-Books-Submit.x=36&Adv-Srch-Books-Submit.y=12&unfiltered=1&ref=sr_adv_b'
        self.driver.get(link)

    def parse(self) -> list[list[str]]:
        wholes = [whole.text for whole in self.driver.find_elements(By.CLASS_NAME, 
                                                            'a-price-whole')]
        fractions = [fraction.text for fraction in self.driver.find_elements(By.CLASS_NAME, 
                                                                        'a-price-fraction')]
        types = [type.text for type in self.driver.find_elements(By.CLASS_NAME,
                                                            'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold')]
        results = []
        for items in zip(wholes, fractions, types):
            results.append([items[2], f'{items[0]}.{items[1]}'])
        return results

if __name__ == '__main__':
    '''some example driver code that takes an isbn
      and prints the parsed information from the results
    '''

    isbn = 9780545091022
    # isbn = 9780062024022
    amazonFetch = Amazon(isbn)
