from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import ssl
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

context = ssl._create_unverified_context()

def get_html_with_click(url, css_selector):
  browser.get(url)
  time.sleep(1)

  browser.find_element(By.CSS_SELECTOR, css_selector).click() 
  time.sleep(1)

  bsObj = BeautifulSoup(browser.page_source, 'html.parser')

  return bsObj


def get_html(url):
  browser.get(url)
  time.sleep(1)
  bsObj = BeautifulSoup(browser.page_source, 'html.parser')

  return bsObj


from theater.cgv import find_cgv_area_code, find_cgv_theater_code
from theater.megabox import find_mbox_theater_code
from theater.lotte import find_lotte_area_code, find_lotte_theater_code

# TODO: URL 정리
cgv_theater_url = 'http://www.cgv.co.kr/theaters/'
mbox_theater_url = 'https://www.megabox.co.kr/theater/list/'
lotte_theater_url = 'https://www.lottecinema.co.kr/'

cgv_area_code = find_cgv_area_code(get_html(cgv_theater_url))
cgv_theater_code = find_cgv_theater_code(get_html(cgv_theater_url))

mbox_theater_code = find_mbox_theater_code(get_html(mbox_theater_url))

lotte_area_code = find_lotte_area_code(get_html(lotte_theater_url))
lotte_theater_code = find_lotte_theater_code(get_html(lotte_theater_url))

from movie.cgv import get_cgv_movie_list
from movie.megabox import get_mbox_movie_list

### TODO: URL 영화관 코드는 REST API Query 로 탐색 (default 지정 필요?)
# TODO: date 예외 처리
cgv_movies_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0001&date=20220128'
mbox_movies_url = 'https://www.megabox.co.kr/theater/time?brchNo=1372'

mbox_btn_selector = 'button[date-data="2022.01.26"]'

cgv_movie_list = get_cgv_movie_list(get_html(cgv_movies_url))
mbox_movie_list = get_mbox_movie_list(get_html_with_click(mbox_movies_url, mbox_btn_selector)) # TODO: date 예외 처리

from screen.cgv import get_cgv_screen_list, get_cgv_screen_movie_list
from screen.megabox import get_mbox_screen_list, get_mbox_screen_movie_list

cgv_screen_list = get_cgv_screen_list(get_html(cgv_movies_url))
cgv_screen_movie_list = get_cgv_screen_movie_list(get_html(cgv_movies_url))

mbox_screen_list = get_mbox_screen_list(get_html_with_click(mbox_movies_url, mbox_btn_selector))
mbox_screen_movie_list = get_mbox_screen_movie_list(get_html_with_click(mbox_movies_url, mbox_btn_selector))
