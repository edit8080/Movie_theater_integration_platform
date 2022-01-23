from urllib.parse import urlparse, parse_qs


def find_lotte_area_code(bsObj):
  area_code_list = []
  theater_section = bsObj.select('#nav > ul > li:nth-child(3) > div > ul > li')

  # 0번은 스페셜관
  for area in theater_section[1:]:
    area_name = area.find('a').get_text()

    theater = area.find('div').find('a')
    href = theater.attrs['href']

    code = parse_qs(urlparse(href).query)

    area_code_list.append({
      'areaCode': code['detailDivisionCode'][0],
      'areaName': area_name
    })

  return area_code_list

def find_lotte_theater_code(bsObj):
  theater_code_list = []
  theater_section = bsObj.select('#nav > ul > li')[2]

  for theater in theater_section.findAll('a'):
    theater_name = theater.get_text()
    href = theater.attrs['href']

    code = parse_qs(urlparse(href).query)

    if 'detailDivisionCode' in code and 'cinemaID' in code:
      theater_code_list.append({
        'areaCode': code['detailDivisionCode'][0],
        'theaterCode': code['cinemaID'][0],
        'theaterName': theater_name
      })

  return theater_code_list

