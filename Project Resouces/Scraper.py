#Andrew Patton
#Christopher Pillgreen

# from bs4 import BeautifulSoup
# import requests
import threading
from functools import partial
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement #referenced but not used
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

class Amazon:
class Amazon:
    threads = []
    def __init__(self, isbn):
        def t():
            self.isbn = isbn
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(2)
            self.search(isbn)
            things = self.parseSearch() + self.parseResult()
            for thing in things:
                print(thing)
            print()
            self.driver.close()
        Amazon.threads.append(threading.Thread(target=t))

    def search(self, isbn: int) -> None:
        link = f'https://www.amazon.com/s?i=stripbooks&rh=p_66%3A\
            {isbn}&s=relevanceexprank&Adv-Srch-Books-Submit.x=36&Adv-Srch-Books-Submit.y=12&unfiltered=1&ref=sr_adv_b'
        self.driver.get(link)

    def parseSearch(self) -> list[list[str]]:
        wholes = [whole.text for whole in self.driver.find_elements(
            By.CLASS_NAME, 'a-price-whole')]
        fractions = [fraction.text for fraction in self.driver.find_elements(
            By.CLASS_NAME, 'a-price-fraction')]
        types = [type.text for type in self.driver.find_elements(
            By.CLASS_NAME,'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold')]
        results = []
        for items in zip(wholes, fractions, types):
            results.append([items[2], f'{items[0]}.{items[1]}'])
        else:
            if len(results) == 0:
                print('Amazon has no such book')
        return results
    
    def parseResult(self):
        results = []
        if not self.driver.find_elements(
            By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base'):
            return results
        
        numFormats = len(
            self.driver.find_element(
            By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base').find_elements(
            By.CLASS_NAME, 'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style'))
        for index in range(numFormats):
            formats = self.driver.find_element(
            By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base').find_elements(
            By.CLASS_NAME, 'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style')
            format = formats[index].text
            formats[index].click()
            try:
                price = self.driver.find_element(
                    By.ID, 'tmmSwatches').find_element(
                    By.CLASS_NAME, 'a-size-base.a-color-price.a-color-price').text[1:]
            except:
                price = 'NULL'
            results.append([format, price])
            self.driver.back()
        return results

def Barnes(isbn):
    
    def __init__(self):
        pass
    pass


if __name__ == '__main__':
    '''some example driver code that takes an isbn
      and prints the parsed information from the results
    '''
# def main():
#     # isbn = 9780545091022
#     # isbn = 9780062024022
#     isbn = 9780060194994
#     # isbn = 9780199608522
#     isbns = [9780060194994, 9780199608522, 9780062024022, 9780545091022]
#     for isbn in isbns:
#         Amazon(isbn)
#     for thread in Amazon.threads:
#         thread.start()
#     for thread in Amazon.threads:
#         thread.join()
#     print('done')

Barnes()