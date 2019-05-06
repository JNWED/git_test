import requests
import json

hotcardid_file=open("./config/hotcardcookie.txt")
line=hotcardid_file.readline()
url="http://qa.igame.163.com/api/backend/livestream/backpack/send"
while line:
    uid=line.strip('\n')
    print uid
    requestData = {'id':52002,'userIds':uid,"amount":5}
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Cookie': cookie_u}
    res1 = requests.post(url, data=requestData, headers=headers)
    print res1.text
    line=hotcardid_file.readline()
hotcardid_file.close()
