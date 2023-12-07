from abc import ABC, abstractmethod
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSelectorException

def runThreads(threads: list[Thread]):
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

class Scraper(ABC):
    threads: list[Thread] = list()
    results = dict()

    @abstractmethod
    def __init__(self, isbn: int):
        pass

    @abstractmethod
    def search(self, isbn: int) -> None:
        pass

    @abstractmethod
    def parse(self) -> list[list[str]]:
        pass

    @property 
    @abstractmethod
    def items(self):
        pass

    def printResults():
        for key in Scraper.results.keys():
            print(key)
            for item in Scraper.results[key]:
                print(item)
            print()

    def run() -> None:
        runThreads(Scraper.threads)
        Scraper.printResults()

class Amazon(Scraper):
    
    url = 'https://www.amazon.com/s?i=stripbooks&rh=p_66%3A{}&s=relevanceexprank&Adv-Srch-Books-Submit.x=36&Adv-Srch-Books-Submit.y=12&unfiltered=1&ref=sr_adv_b'
    def __init__(self, isbn: int):
        def t():
            '''func to be run simultaneously with other subclasses of Scraper'''
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)

        self.search(isbn)

        Scraper.results['Amazon'] = self.parse()
        Scraper.results['Amazon'] += self.parseResults()

        Scraper.threads.append(Thread(target = t))

    def search(self, isbn: int) -> None:
        '''initializes page'''
        self.driver.get(Amazon.url.format(isbn))

    def parse(self) -> list[list[str, str, str]]: 
        '''returns [[Amazon, Format, Price], ...]'''
        results = []

        wholes = [whole.text for whole in self.driver.find_elements(
            By.CLASS_NAME, 'a-price-whole')]
        fractions = [fraction.text for fraction in self.driver.find_elements(
            By.CLASS_NAME, 'a-price-fraction')]
        types = [type.text for type in self.driver.find_elements(
            By.CLASS_NAME,'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-bold')]

        for items in zip(types, wholes, fractions):
            results.append([items[0], f'{items[1]}.{items[2]}'])

        return results

    def parseResults(self) -> list[list[str, str, str]]:
        '''returns [[Amazon, Format, Price], ...]'''
        results = []
        links = ['Buffer']
        prices = []
        threads = []
        if self.driver.find_elements(By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base'):
            formatElements = self.driver.find_element(
            By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base').find_elements(
            By.CLASS_NAME, 'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style')
            
            formatNames = [element.text for element in self.driver.find_element(
                       By.CLASS_NAME, 'a-row.a-spacing-top-micro.a-size-small.a-color-base').find_elements(
                       By.CLASS_NAME, 'a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style')]
            
            for element in formatElements:
                links.append(element.get_property('href'))

            for index in range(1, len(links)): #starts at 1 because of the buffer (initial site)
                self.driver.execute_script("window.open('');")
                self.driver.switch_to.window(self.driver.window_handles[index])
                self.driver.get(links[index])
                try:
                    prices.append(self.driver.find_element(
                        By.ID, 'tmmSwatches').find_element(
                        By.CLASS_NAME, 'a-size-base.a-color-price.a-color-price').text[1:])
                except InvalidSelectorException:
                    print('has been reached')
                    prices.append('NULL')
            runThreads(threads)
                

            for pair in zip(formatNames, prices):
                results.append([pair[0], pair[1]])

        return results
    
    @property
    def items(self):
        return self.items

class Barnes(Scraper):
    url = 'https://www.barnesandnoble.com/'
    
    def __init__(self, isbn: int):
        def t():
            '''func to be run simultaneously with other subclasses of Scraper'''
            pass
        Scraper.threads.append(t)

    def search(self, isbn: int) -> None:
        '''initializes page'''
        return

    def parse(self) -> list[list[str, str]]:
        '''returns [[Barnes&Noble, Format, Price], ...]'''
        results = []
        return results
    
    def parseResults(self) -> list[list[str, str, str]]:
        '''returns [[Amazon, Format, Price], ...]'''
        results = []
        return results
    
    @property
    def items(self):
        return self.items
    
class Title:
    url = 'https://isbndb.com/book/{}'
    pass



Amazon(9780060194994)
Scraper.run()

