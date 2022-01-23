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

# TODO: date 예외 처리
cgv_movies_url = 'http://www.cgv.co.kr/common/showtimes/iframeTheater.aspx?areacode=01&theatercode=0001&date=20220126'

cgv_movie_list = get_cgv_movie_list(get_html(cgv_movies_url))

from screen.cgv import get_cgv_screen_list, get_cgv_screen_movie_list

cgv_screen_list = get_cgv_screen_list(get_html(cgv_movies_url))
cgv_screen_movie_list = get_cgv_screen_movie_list(get_html(cgv_movies_url))
