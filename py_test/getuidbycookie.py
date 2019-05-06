import requests
import json

cookie_file=open("./config/avar_cookie.txt")
line=cookie_file.readline()
url="http://qa.igame.163.com/api/livestream/personalpage/about"
while line:
    cookie_u=line.strip('\n')
    #print cookie_u
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Cookie': cookie_u}
    res1 = requests.post(url,  headers=headers)
    restext=res1.text
    resjson=json.loads(restext)
    #print resjson
    if not resjson.get('data') is None :
        print resjson.get('data').get('userId'),
    line=cookie_file.readline()
cookie_file.close()