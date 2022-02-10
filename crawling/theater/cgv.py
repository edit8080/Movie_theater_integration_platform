from urllib.parse import urlparse, parse_qs


# 지역 코드 (서울 - 01)
def find_cgv_area_code(bsObj):
  area_list = []
  cities = bsObj.select('.sect-city > ul > li')

  for area in cities:
    area_name = area.select('a[href="#"]')[0].get_text()
    theater = area.select('.area')[0].find('a')

    href = theater.attrs['href']
    code = parse_qs(urlparse(href).query)

    # TODO : 일부 지역 코드 분리 (ex: 부산/울산 - 05,207)
    area_list.append({
      'area_code': code['areacode'][0],
      'area_name': area_name,
    })

  return area_list

# 영화관 코드 (CGV 강남 - 01 > 0056)
def find_cgv_theater_code(bsObj):
  theater_list = []
  area_list = bsObj.select('.area')

  for area in area_list:
    for theater in area.findAll('a'):
      name = theater.attrs['title']
      href = theater.attrs['href']

      code = parse_qs(urlparse(href).query)

      if 'areacode' in code and 'theaterCode' in code:
        theater_list.append({
          'area_code': code['areacode'][0],
          'theater_id': code['theaterCode'][0],
          'theater_name': name,
        })

  return theater_list

