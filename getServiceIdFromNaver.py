import json
import requests
from bs4 import BeautifulSoup

def getServiceIdFromNaver():
  """
  각 채널의 네이버 ServiceId를 파싱합니다. \n
  @return [ 
    {'Name': '채널이름', 'Id': 'ServiceId'},
    {'Name': '또다른채널이름', 'Id': 'anotherServiceId'}
  ]
  """

  UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
  category = [
    {'name': '지상파', 'u1':'100'},
    {'name': '종합 편성', 'u1': '500'},
    {'name': '케이블', 'u1': '200'},
    {'name': '스카이라이프', 'u1': '300'},
    {'name': '해외위성', 'u1': '9000'},
    {'name': '라디오', 'u1': '400'}
  ]

  result = []
  for cat in category:
    req = requests.get("https://m.search.naver.com/p/csearch/content/nqapirender.nhn?pkid=66&where=nexearch&u1=%s&key=ScheduleChannelList" % cat['u1'], headers={'User-Agent': UA})
    print('Status Code: ', req.status_code)

    html = BeautifulSoup(json.loads(req.text)['dataHtml'], 'html.parser')
    channels = html.select('li.item')

    for channel in channels:
      serviceId = channel.find('div', attrs={'class': "u_likeit_list_module _reactionModule zzim"})['data-cid']
      ch_name = channel.find('div', attrs={'class': "channel_name"}).string
      result.append({'Name': ch_name, 'Id': serviceId})
  
  return result
