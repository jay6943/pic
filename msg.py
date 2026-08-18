import os
import sys
import time
import requests
import datetime as dt


def send_discord_message(message):
  # url = 'https://discord.com/api/webhooks/1516685405100052500'
  # key = 'wfEAmZeZq2oHwPzNUsn2u2n-d60BApE8kSZgPWyDxaxbV2zbH_3z2j-HaPoCDI3MJRCr'
  url = 'https://discord.com/api/webhooks/1538826593471037482'
  key = 'R34AURoT8-pI71knDrMbCWc4EeI83ObJpYywAsZk_XMNSDitW7buCZOciKJZpLLvkmO6'
  payload = {'content': message}
  response = requests.post(f'{url}/{key}', json=payload)
  if response.status_code == 204: print('메시지가 성공적으로 전송되었습니다!')
  else: print(f'전송 실패: 상태 코드 {response.status_code}')


def strtime(at):
  return at.strftime('%H:%M:%S')
  

def is_completed(filepath):
  if not os.path.isfile(filepath):
    print(f'Error, no {filepath}')
    return 1
  
  start = dt.datetime.now()
  filename = filepath.split('/')[-1][:-7]
  print(f'{strtime(start)}, {filename} 시뮬레이션 시작')

  i_counting = 0
  check_completed = True
  while check_completed:
    time.sleep(600)
    fp = open(filepath, 'r', encoding='utf-8')
    for line in fp:
      if 'Simulation completed successfully' in line:
        check_completed = False
    i_counting += 1
    if check_completed and i_counting > 5:
      texts = f'{line.split('complete.')[0]}'
      send_discord_message(f'시뮬레이션 진행률, {texts}')
      i_counting = 0
    fp.close()
    if check_completed:
      print(f'{strtime(dt.datetime.now())}, {line.split('. ')[0]}.')
  
  stop = dt.datetime.now()
  print(f'시뮬레이션 시간, {str(stop - start).split('.')[0]}')
  
  send_discord_message(f'{strtime(stop)}, 시뮬레이션 완료\n{filename}')
  
  return 0


if __name__ == '__main__': is_completed(f'{sys.argv[1]}.log')
