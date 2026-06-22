import sys
import time
import requests
import datetime as dt


def strtime(at):
  return at.strftime('%H:%M:%S')
  

def check_process(filepath):
  start = dt.datetime.now()
  fp = filepath.split('/')[-1][:-7]
  print(f'{strtime(start)}, {fp} 시작')
  check_completed = True
  while check_completed:
    time.sleep(600)
    fp = open(filepath, 'r', encoding='utf-8')
    for line in fp:
      if 'Simulation completed successfully' in line:
        check_completed = False
    fp.close()
    if check_completed:
      print(f'{strtime(dt.datetime.now())}, {line.split('. ')[0]}.')
  stop = dt.datetime.now()
  print(f'시뮬레이션 시간, {str(stop - start).split('.')[0]}')
  send_discord_message(f'{strtime(stop)}, {fp} 완료')


def send_discord_message(message):
  url = 'https://discord.com/api/webhooks/1516685405100052500'
  key = 'wfEAmZeZq2oHwPzNUsn2u2n-d60BApE8kSZgPWyDxaxbV2zbH_3z2j-HaPoCDI3MJRCr'
  payload = {'content': message}
  response = requests.post(f'{url}/{key}', json=payload)
  if response.status_code == 204: print('메시지가 성공적으로 전송되었습니다!')
  else: print(f'전송 실패: 상태 코드 {response.status_code}')


if __name__ == '__main__': check_process(f'{sys.argv[1]}.log')
