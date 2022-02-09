from datetime import datetime
from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  lotteMovieCode: String, 
  movieTitle: String,
  moviePlayTime: Number,
  movieGrade: Number
}
"""

def check_movie_grade(node):
  className = node.attrs['class']

  if 'gr_all' in className:
    return 0

  elif 'gr_12' in className:
    return 12

  elif 'gr_15' in className:
    return 15
  
  elif 'gr_18' in className:
    return 18

def hhmm_diff_minutes(start, end):
  fmt = '%H:%M'

  start_date = datetime.strptime(start, fmt)
  end_date = datetime.strptime(end, fmt)

  return int((end_date - start_date).total_seconds() / 60)

def get_lotte_movie_list(bsObj):
  movie_list = []

  for movie_section in bsObj.select('.time_select_wrap'):
    movie_info_section = movie_section.find('div', {'class': 'list_tit'})

    movie_icon = movie_info_section.find('span', {'class': 'ic_grade'})
    movie_grade = check_movie_grade(movie_icon)

    movie_title = movie_info_section.find('p').get_text().strip()

    href = movie_info_section.find('a').attrs['href']
    code = parse_qs(urlparse(href).query)

    time_info = movie_section.find('ul', {'class': 'list_time'}).find('dd', {'class': 'time'}).get_text().strip()

    parse_str = parse('{movie_start_time}종료 {movie_end_time}', time_info)  

    movie_list.append({
      'lotteMovieCode': code['movie'][0],
      'movieTitle': movie_title,
      'moviePlayTime': hhmm_diff_minutes(parse_str['movie_start_time'], parse_str['movie_end_time']),
      'movieGrade': int(movie_grade)
    })

  return movie_list

