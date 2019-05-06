import requests
import json
import jsonpath


#getcookie
cookie_file=open("./config/hotcartcookie.txt")
line=cookie_file.readline()
#sendhotcarturl
url='http://qa.igame.163.com/api/livestream/backpack/present'
#getpackid
packid_file=open("./config/packid.txt")
packid_line=packid_file.readline()


#getliveid
recurl='http://qa.igame.163.com/api/livestream/homepage/recommend'
cookie_u='MUSIC_U=baf0583f6bcce48ac15feaaa826ce384d571b19c04b1d5f729ead26780b565e39bffab2f04a1ae7cae2f3fa972ecb108088482c38940710e;os=iphone'
headers = {'content-type': 'application/x-www-form-urlencoded', 'Cookie': cookie_u}
recres=requests.get(recurl,headers=headers)
recrestext=recres.text
recresjson=json.loads(recrestext)
liveid_list=jsonpath.jsonpath(recresjson,"$..liveId")
for liveid in liveid_list:
    cookie_h=line.strip('\n')
    packid=packid_line.strip('\n')
    requestData = {'id':packid,'liveId':liveid,'number':1,'batch':0 }
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Cookie': cookie_h}
    res1 = requests.post(url, data=requestData, headers=headers)
    print res1.text
    line=cookie_file.readline()
    packid_line=packid_file.readline()

cookie_file.close()



