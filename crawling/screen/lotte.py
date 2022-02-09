from urllib.parse import urlparse, parse_qs
from parse import *


"""
{
  theaterCode: String ('1372'),
  screenCode: String ('2'),
  screenName: String ('2관'), 
  totalSeat: Number (103),
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
          'theaterCode': theater_code['cinemaID'][0],
          'screenCode': screen_str['screen_code'],
          'screenName': screen_name,
          'totalSeat': int(parse_seat['total_seat'])
        })
        break
  
  return screen_list
  

"""
{
  lotteMovieCode: String ('18407'),
  screenCode: String ('2'),
  screenType: String ('2D'),
  leftSeat: Number (70),
  movieStartTime: String ('08:20'),
  movieEndTime: String ('10:36'),
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
          'lotteMovieCode': movie_code['movie'][0],
          'screenCode': parse_screen['screen_code'],
          'screenType': screen_type,
          'leftSeat': int(parse_seat['left_seat']),
          'movieStartTime': parse_time['start_time'],
          'movieEndTime': parse_time['end_time'],
        })

  return screen_movie_list

