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


from theaters.cgv import find_cgv_area_code, find_cgv_theater_code
from theaters.megabox import find_mbox_theater_code

cgv_theater_url = 'http://www.cgv.co.kr/theaters/'
mbox_theater_url = 'https://www.megabox.co.kr/theater/list/'

cgv_area_code = find_cgv_area_code(get_html(cgv_theater_url))
cgv_theater_code = find_cgv_theater_code(get_html(cgv_theater_url))

mbox_theater_code = find_mbox_theater_code(get_html(mbox_theater_url))

