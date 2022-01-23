from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  theaterCode: String,
  screenCode: String,
  screenType: String,
  screenName: String,
  totalSeat: Number,
}
"""
def get_cgv_screen_list(bsObj):
  screen_list = []

  for hall_time_section in bsObj.select('.type-hall'):
    hall_info = hall_time_section.find('div', {'class': 'info-hall'}).findAll('li')

    # TODO: screen_type 정규화 고민 (동일한 관에 2D(더빙), 2D(자막) 가능)
    screen_type = hall_info[0].get_text().strip()
    screen_name = hall_info[1].get_text().strip()
    hall_info_str = parse('총{total_seat}석', ''.join(hall_info[2].get_text().split()))

    total_seat = hall_info_str['total_seat']

    time_info = hall_time_section.find('div', {'class': 'info-timetable'}).find('a')
    screen_code = time_info.attrs['data-screencode']

    screen_list.append({
      'screenCode': screen_code,
      'screenType': screen_type,
      'screenName': screen_name,
      'totalSeat': int(total_seat),
    })

  return screen_list


"""
{
  cgvMovieCode: String,
  screenCode: String,
  leftSeat: Number,
  movieStartTime: String,
  movieEndTime: String,
  canReserve: Boolean
}
"""
def get_cgv_screen_movie_list(bsObj):
  screen_movie_list = []

  for hall_time_info in bsObj.select('.col-times'):
    href = hall_time_info.find('div', {'class': 'info-movie'}).find('a').attrs['href']
    movie_code = parse_qs(urlparse(href).query)

    for time_info in hall_time_info.find('div', {'class': 'info-timetable'}).findAll('a'):
      screen_code = time_info.attrs['data-screencode']
      movie_start_time = time_info.attrs['data-playstarttime']
      movie_end_time = time_info.attrs['data-playendtime']

      left_seat_parse = parse('잔여좌석{left_seat}석', time_info.find('span').get_text())

      ## TODO: 매진 됐을 때 canReserve와 left_seat 가 정상동작하는지 확인
      screen_movie_list.append({
        'cgvMovieCode': movie_code['midx'][0],
        'screenCode': screen_code,
        'leftSeat': int(left_seat_parse['left_seat']),
        'movieStartTime': movie_start_time,
        'movieEndTime': movie_end_time,
        'canReserve': left_seat_parse['left_seat'] == 0 if False else True
      })

  return screen_movie_list
