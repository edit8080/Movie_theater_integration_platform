from urllib.parse import urlparse, parse_qs
from parse import *


"""
{
  theater_id: String ('1372'),
  screen_id: String ('2'),
  screen_name: String ('2관'), 
  total_seat: Number (103),
}
"""
def get_lotte_screen_list(bsObj, url):
  screen_list = []
  theater_code = parse_qs(urlparse(url).query)
    
  for time_select_section in bsObj.select('.time_select_wrap'):
    for time_list in time_select_section.select('.list_time'):
      for time_section in time_list.select('li'):
        seat_str = time_section.find('dd', {'class': 'seat'}).get_text().strip()
        parse_seat = parse('{left_seat} / {total_seat}', seat_str)

        # 매진 -> 다음 시간표 탐색
        if parse_seat is None: 
          continue

        screen_name = time_section.find('dd', {'class': 'hall'}).get_text().strip()
        screen_str = parse('{screen_code}관', screen_name)

        # 스크린 정보 하나 삽입되면 시간표 탐색 종료
        screen_list.append({
          'theater_id': theater_code['cinemaID'][0],
          'screen_id': screen_str['screen_code'],
          'screen_name': screen_name,
          'total_seat': int(parse_seat['total_seat'])
        })
        break
  
  return screen_list
  

"""
{
  lotte_movie_id: String ('18407'),
  screen_id: String ('2'),
  screen_type: String ('2D'),
  left_seat: Number (70),
  start_time: String ('08:20'),
  end_time: String ('10:36'),
}
"""
def get_lotte_screen_movie_list(bsObj):
  screen_movie_list = []

  for time_select_section in bsObj.select('.time_select_wrap'):
    movie_link = time_select_section.find('div', {'class': 'list_tit'}).find('a')
    movie_code = parse_qs(urlparse(movie_link.attrs['href']).query)

    screen_type = time_select_section.find('ul', {'class': 'list_hall'}).find('li').get_text().strip()

    for time_list in time_select_section.select('.list_time'):
      screen_name = time_list.find('dd', {'class': 'hall'}).get_text().strip()
      parse_screen = parse('{screen_code}관', screen_name)

      for time_section in time_list.select('li'):
        seat_str = time_section.find('dd', {'class': 'seat'}).get_text().strip()
        parse_seat = parse('{left_seat} / {total_seat}', seat_str)

        # 매진
        if parse_seat is None: 
          continue

        time_info = time_section.find('dd', {'class': 'time'}).get_text().strip()
        parse_time = parse('{start_time}종료 {end_time}', time_info)

        screen_movie_list.append({
          'lotte_movie_id': movie_code['movie'][0],
          'screen_id': parse_screen['screen_code'],
          'screen_type': screen_type,
          'left_seat': int(parse_seat['left_seat']),
          'start_time': parse_time['start_time'],
          'end_time': parse_time['end_time'],
        })

  return screen_movie_list

