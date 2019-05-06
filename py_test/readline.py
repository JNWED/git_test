import requests
import json

cookie_file=open("./config/avar_cookie.txt")
avarid_file=open("./config/avarid.txt")
line=cookie_file.readline()
line_avar=avarid_file.readline()
url="http://qa.igame.163.com/api/livestream/user/profile/update"
url_get="http://qa.igame.163.com/api/livestream/personalpage/userinfo"
while line:
    b=line_avar
    print b
    cookie_u=line.strip('\n')
    print cookie_u
    requestData = {'avatarImgId':b }
    headers = {'content-type': 'application/x-www-form-urlencoded', 'Cookie': cookie_u}
    res1 = requests.post(url, data=requestData, headers=headers)
    res2 = requests.get(url_get, headers=headers)
    print res1.text
    print res2.text
    line=cookie_file.readline()
    line_avar=avarid_file.readline()
cookie_file.close()
avarid_file.close()