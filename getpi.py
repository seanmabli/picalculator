import requests

open('pi.txt', "w").write('')
pi = ''
for i in range(1000):
  pi += requests.get('https://api.pi.delivery/v1/pi?start=' + str(i * 1000) + '&numberOfDigits=1000').json()["content"]
  open('pi.txt', "a").write(pi)