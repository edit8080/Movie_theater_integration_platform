from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import ssl


options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

context = ssl._create_unverified_context()

def get_html(url):
  browser.get(url)
  bsObj = BeautifulSoup(browser.page_source, 'html.parser')

  return bsObj


from theaters.cgv import find_area_code, find_theater_code

cgv_area_code = find_area_code(get_html('http://www.cgv.co.kr/theaters/'))
cgv_theater_code = find_theater_code(get_html('http://www.cgv.co.kr/theaters/'))

