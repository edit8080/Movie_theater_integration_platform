from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  theater_id: String ('1372'),
  screen_id: String ('02'),
  screen_name: String ('2관'), 
  total_seat: Number (103),
}
"""
def get_mbox_screen_list(bsObj, url):
  screen_list = []
  url_query = parse_qs(urlparse(url).query)

  for hall_time_section in bsObj.select('.theater-list'):
    hall_section = hall_time_section.find('div', {'class': 'theater-type-box'})

    time_table_td = hall_section.find('table', {'class': 'time-list-table'}).find('td')

    # 매진 (정보 x)
    if not 'theab-no' in time_table_td.attrs:
      continue

    screen_code = time_table_td.attrs['theab-no']

    screen_name = hall_section.find('p', {'class': 'theater-name'}).get_text().strip()

    total_seat = hall_section.find('p', {'class': 'chair'}).get_text().strip()
    total_seat_str = parse('총 {total_seat}석', total_seat)

    screen_list.append({
      'theater_id': url_query['brchNo'][0],
      'screen_id': screen_code,
      'screen_name': screen_name,
      'total_seat': int(total_seat_str['total_seat'])
    })

  return screen_list

"""
{
  mbox_movie_id: String ('21089100'),
  screen_id: String ('02'),
  screen_type: String ('2D'),
  left_seat: Number (70),
  start_time: String ('08:20'),
  end_time: String ('10:36'),
}
"""
def get_mbox_screen_movie_list(bsObj):
  screen_movie_list = []

  for hall_time_section in bsObj.select('.theater-list'):
    hall_section = hall_time_section.find('div', {'class': 'theater-type-box'})

    time_table_td = hall_section.find('table', {'class': 'time-list-table'}).find('td')

    # 매진 (정보 x) - 예약 가능한 정보만 저장
    if not 'brch-no' in time_table_td.attrs:
      continue

    movie_code = time_table_td.attrs['rpst-movie-no']
    screen_code = time_table_td.attrs['theab-no']

    left_seat = time_table_td.find('p', {'class': 'chair'}).get_text().strip()
    left_seat_str = parse('{left_seat}석', left_seat)

    movie_time = time_table_td.find('div', {'class': 'play-time'}).find('p').get_text().strip()
    movie_time_str = parse('{start_time}~{end_time}', movie_time)

    screen_type = hall_section.find('div', {'class': 'theater-type-area'}).get_text().strip()

    screen_movie_list.append({
      'mbox_movie_id': movie_code,
      'screen_id': screen_code,
      'screen_type': screen_type,
      'left_seat': int(left_seat_str['left_seat']),
      'start_time': movie_time_str['start_time'],
      'end_time': movie_time_str['end_time'],
    })

  return screen_movie_list

