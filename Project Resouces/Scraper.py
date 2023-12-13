from abc import ABC, abstractmethod
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
OPTIONS = Options()
OPTIONS.add_argument(f'user-agent={agent}')
OPTIONS.add_argument('--headless=new')
OPTIONS.add_argument('--window-size=1920,1080')

class Scraper(ABC):

    results = {'Amazon':[['', '']],
               'Barnes':[['', '']],
               'Books-A-Million':[['', '']],}
            #    'Google':[['', '']]}

    title = ''

    @abstractmethod
    def __init__(self, isbn: int):
        pass

    @abstractmethod
    def search(self, isbn: int) -> None:
        pass

    @abstractmethod
    def parse(self) -> list[list[str]]:
        pass

class Amazon(Scraper):
    url = 'https://www.amazon.com/s?i=stripbooks&rh=p_66%3A{}&s=relevanceexprank&Adv-Srch-Books-Submit.x=36&Adv-Srch-Books-Submit.y=12&unfiltered=1&ref=sr_adv_b'
    
    def __init__(self, isbn: int):
        self.driver = webdriver.Chrome(OPTIONS)
        self.driver.implicitly_wait(1)
        self.search(isbn)
        Scraper.results['Amazon'] = self.parse()
        Scraper.results['Amazon'] += self.parseResults()

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
            results.append([items[0], f'${items[1]}.{items[2]}'])

        return results

    def parseResults(self) -> list[list[str, str, str]]:
        '''returns [[Amazon, Format, Price], ...]'''
        results = []
        links = ['Buffer']
        prices = []
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
                except NoSuchElementException:
                    print('has been reached')
                    prices.append('NULL')

            for pair in zip(formatNames, prices):
                results.append([pair[0], pair[1]])

        return results

class Barnes(Scraper):
    url = 'https://www.barnesandnoble.com/'
    
    def __init__(self, isbn: int):
        self.driver = webdriver.Chrome(OPTIONS)
        self.driver.implicitly_wait(1)
        self.search(isbn)
        Scraper.results['Barnes'] = self.parse()

    def search(self, isbn: int) -> None:
        '''initializes page'''
        self.driver.get(Barnes.url)
        searchBar = self.driver.find_element(By.TAG_NAME, 'nav').find_element(By.TAG_NAME, 'input')
        searchBar.send_keys(str(isbn))
        button = self.driver.find_element(By.CLASS_NAME,'btn.btn-outline-secondary.rhf-search-btn')
        button.click()

    def parse(self) -> list[list[str, str]]:
        '''returns [[Format, Price], ...]'''
        results = []
        prices = [price.text for price in self.driver.find_elements(By.CLASS_NAME, 'format-price')]
        types = [type.text for type in self.driver.find_elements(By.CLASS_NAME, 'span-with-normal-white-space')]
        for price, book_type in zip(prices, types):
            results.append([book_type, price])
        return results

# attempted google class, but
# html class id's are unique to each book
# no unifying class to grab data
'''
class Google(Scraper):
    url = 'https://play.google.com/store/books?hl=en&gl=US'

    def __init__(self): # may instantiate title class later
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(1)
        self.search(Scraper.title)
        Scraper.results['Google'] = self.parse()

    def search(self, title: str) -> None:
        self.driver.get(Google.url)
        searchButton = self.driver.find_element(By.CLASS_NAME, 'google-material-icons.r9optf')
        searchButton.click()
        searchBar = self.driver.find_element(By.CLASS_NAME, 'HWAcU')
        searchBar.send_keys(str(title))
        searchBar.send_keys(Keys.RETURN)

    def parse(self) -> list[list[str, str]]:
        results = []
        prices = [price.text for price in self.driver.find_elements(By.CLASS_NAME, 'VfPpfd VixbEe')]
        types = [type.text for type in self.driver.find_elements(By.CLASS_NAME, 'kcen6d')]
        for price, book_type in zip(prices, types):
            results.append([book_type, price])
            print(results)
        return results
'''
       
class Million(Scraper):
    url = 'https://www.booksamillion.com/'

    def __init__(self, isbn: int):
        self.driver = webdriver.Chrome(OPTIONS)
        self.driver.implicitly_wait(1)
        self.search(isbn)
        Scraper.results['Books-A-Million'] = self.parse()

    def search(self, isbn: int) -> None:
        self.driver.get(Million.url)
        searchBar = self.driver.find_element(By.CLASS_NAME, 'search-wrapper').find_element(By.CLASS_NAME, 'ui-autocomplete-input')
        searchBar.send_keys(str(isbn))
        button = self.driver.find_element(By.ID,'searchIcon').find_element(By.TAG_NAME, 'i')
        button.click()

    def parse(self) -> list[list[str]]:

        results = []
        prices = [price.text for price in self.driver.find_elements(By.CLASS_NAME, 'our-price')]
        types = [type.text for type in self.driver.find_elements(By.CLASS_NAME, 'productInfoText')]
        for price, book_type in zip(prices, types):
            results.append([book_type, price])
        return results

class Title(Scraper):
    url = 'https://isbndb.com/book/{}'
    
    def __init__(self, isbn):
        self.driver = webdriver.Chrome(OPTIONS)
        self.driver.implicitly_wait(1)
        self.search(isbn)
        Scraper.title = self.parse()

    def parse(self):
        pass

    def search(self, isbn: int) -> None:
        self.driver.get(Title.url.format(isbn))

    def parse(self):
        title = self.driver.find_element(
            By.CLASS_NAME, 'region.region-page-title').find_element(
            By.TAG_NAME, 'h1').text
        return title
    