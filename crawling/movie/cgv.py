from urllib.parse import urlparse, parse_qs
from parse import *

"""
{
  cgv_movie_id: String, 
  movie_title: String,
  play_time: Number,
  movie_grade: Number
}
"""

def check_movie_grade(node):
  className = node.attrs['class']

  if 'grade-all' in className:
    return 0

  elif 'grade-12' in className:
    return 12

  elif 'grade-15' in className:
    return 15
  
  elif 'grade-18' in className:
    return 18


def get_cgv_movie_list(bsObj):
  movie_list = []

  for movie_info_section in bsObj.select('.info-movie'):
    movie_icon = movie_info_section.find('span', {'class': 'ico-grade'})
    movie_grade = check_movie_grade(movie_icon)

    movie_title = movie_info_section.find('strong').get_text().strip()

    href = movie_info_section.find('a').attrs['href']
    code = parse_qs(urlparse(href).query)

    play_time_str = movie_info_section.select('i')[1].get_text().strip()
    parse_str = parse('{movie_play_time}분', play_time_str)  

    movie_list.append({
      'cgv_movie_id': code['midx'][0],
      'movie_title': movie_title,
      'play_time': int(parse_str['movie_play_time']),
      'movie_grade': movie_grade
    })

  return movie_list
