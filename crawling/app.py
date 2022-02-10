from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("--disable-popup-blocking")
browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

def get_html_with_click(url, css_selector, alert_remove=False):
  browser.get(url)
  time.sleep(1)

  if alert_remove:
    br = Alert(browser)
    br.accept()
    time.sleep(1)

  browser.execute_script("arguments[0].click();", WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))))
  time.sleep(1)
  bsObj = BeautifulSoup(browser.page_source, 'html.parser')

  return bsObj


def get_html(url):
  browser.get(url)
  time.sleep(1)
  bsObj = BeautifulSoup(browser.page_source, 'html.parser')

  return bsObj

### TODO: 모듈 분리 (theater, movie, screen)

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
from movie.lotte import get_lotte_movie_list

# TODO: 각 영화관 url date 예외 처리 (url, click_selector)
cgv_movies_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0001&date=20220212'
mbox_movies_url = 'https://www.megabox.co.kr/theater/time?brchNo=1372'
lotte_movies_url = 'https://www.lottecinema.co.kr/NLCHS/Cinema/Detail?divisionCode=1&detailDivisionCode=1&cinemaID=9094'


mbox_click_selector = 'button[date-data="2022.02.10"]'
lotte_click_selector = '.owl-item:nth-child(3) input[type=radio]'

cgv_movie_list = get_cgv_movie_list(get_html(cgv_movies_url))
mbox_movie_list = get_mbox_movie_list(get_html_with_click(mbox_movies_url, mbox_click_selector)) 
lotte_movie_list = get_lotte_movie_list(get_html_with_click(lotte_movies_url, lotte_click_selector, True))


from screen.cgv import get_cgv_screen_list, get_cgv_screen_movie_list
from screen.megabox import get_mbox_screen_list, get_mbox_screen_movie_list
from screen.lotte import get_lotte_screen_list, get_lotte_screen_movie_list

cgv_screen_list = get_cgv_screen_list(get_html(cgv_movies_url), cgv_movies_url)
cgv_screen_movie_list = get_cgv_screen_movie_list(get_html(cgv_movies_url))

mbox_screen_list = get_mbox_screen_list(get_html_with_click(mbox_movies_url, mbox_click_selector), mbox_movies_url)
mbox_screen_movie_list = get_mbox_screen_movie_list(get_html_with_click(mbox_movies_url, mbox_click_selector))

lotte_screen_list = get_lotte_screen_list(get_html_with_click(lotte_movies_url, lotte_click_selector, True), lotte_movies_url)
lotte_screen_movie_list = get_lotte_screen_movie_list(get_html_with_click(lotte_movies_url, lotte_click_selector, True))
