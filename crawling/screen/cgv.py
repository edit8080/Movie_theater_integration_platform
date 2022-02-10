from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  theater_id: String ('0001'),
  screen_id: String ('011'),
  screen_name: String ('4관'),
  total_seat: Number (34),
}
"""
def get_cgv_screen_list(bsObj, url):
  screen_list = []
  # TODO: url parse -> theaterCode
  url_query = parse_qs(urlparse(url).query)

  for hall_time_section in bsObj.select('.type-hall'):
    time_info = hall_time_section.find('div', {'class': 'info-timetable'}).find('a')

    # 매진
    if time_info is None:
      continue

    screen_code = time_info.attrs['data-screencode']

    hall_info = hall_time_section.find('div', {'class': 'info-hall'}).findAll('li')

    screen_name = hall_info[1].get_text().strip()
    hall_info_str = parse('총{total_seat}석', ''.join(hall_info[2].get_text().split()))

    total_seat = hall_info_str['total_seat']

    screen_list.append({
      'theater_id': url_query['theatercode'][0],
      'screen_id': screen_code,
      'screen_name': screen_name,
      'total_seat': int(total_seat),
    })

  return screen_list


"""
{
  cgv_movie_id: String ('83739'),
  screen_id: String ('011'),
  screen_type: String ('2D'),
  left_seat: Number (34),
  start_time: String ('0930'),
  end_time: String ('1147'),
}
"""
def get_cgv_screen_movie_list(bsObj):
  screen_movie_list = []

  for hall_time_info in bsObj.select('.col-times'):
    href = hall_time_info.find('div', {'class': 'info-movie'}).find('a').attrs['href']
    movie_code = parse_qs(urlparse(href).query)

    for type_hall in hall_time_info.select('.type-hall'):
      screen_type = type_hall.find('div', {'class': 'info-hall'}).find('li').get_text().strip()

      for time_info in type_hall.find('div', {'class': 'info-timetable'}).select('a'):
        screen_code = time_info.attrs['data-screencode']
        movie_start_time = time_info.attrs['data-playstarttime']
        movie_end_time = time_info.attrs['data-playendtime']

        left_seat_parse = parse('잔여좌석{left_seat}석', time_info.find('span').get_text())

        screen_movie_list.append({
          'cgv_movie_id': movie_code['midx'][0],
          'screen_id': screen_code,
          'screen_type': screen_type,
          'left_seat': int(left_seat_parse['left_seat']),
          'start_time': movie_start_time,
          'end_time': movie_end_time,
        })

  return screen_movie_list
