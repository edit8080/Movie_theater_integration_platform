from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  mboxMovieCode: String, 
  movieTitle: String,
  moviePlayTime: Number,
  movieGrade: Number
}
"""

def check_movie_grade(node):
  className = node.attrs['class']

  if 'age-all' in className:
    return 0

  elif 'age-12' in className:
    return 12

  elif 'age-15' in className:
    return 15
  
  elif 'age-19' in className:
    return 18



def get_mbox_movie_list(bsObj):
  movie_list = []

  for movie_info_section in bsObj.select('.theater-list'):
    movie_icon = movie_info_section.find('p', {'class': 'movie-grade'})
    movie_grade = check_movie_grade(movie_icon)

    movie_info = movie_info_section.find('a')
    movie_title = movie_info.get_text().strip()

    href = movie_info.attrs['href']
    code = parse_qs(urlparse(href).query)

    play_time_str = movie_info_section.find('p', {'class': 'infomation'}).get_text().strip()
    playing_str = movie_info_section.find('p', {'class': 'infomation'}).find('span').get_text().strip()
    parse_str = parse('%s/상영시간 {movie_play_time}분' % playing_str, play_time_str) 

    movie_list.append({
      'mboxMovieCode': code['rpstMovieNo'][0],
      'movieTitle': movie_title,
      'moviePlayTime': int(parse_str['movie_play_time']),
      'movieGrade': movie_grade
    })

  return movie_list

