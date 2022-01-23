from urllib.parse import urlparse, parse_qs

# TODO: 지역 코드 통일 필요
# 지역 코드 (서울 - 01)
def find_mbox_area_code(bsObj):
  pass

# 영화관 코드 ()
def find_mbox_theater_code(bsObj):
  theater_code_list = []
  theater_section = bsObj.select('.theater-place > ul > li')

  for area_section in theater_section:
    area_name  = area_section.find('button').get_text().strip()
    theater_list = area_section.find('div', {'class': 'theater-list'}).findAll('a')

    for theater in theater_list:
      theater_name = theater.get_text()
      href = theater.attrs['href']
      code = parse_qs(urlparse(href).query)

      if 'brchNo' in code:
        theater_code_list.append({
          'areaName': area_name,
          'theaterCode': code['brchNo'][0],
          'theaterName': theater_name,
        })

  return theater_code_list

