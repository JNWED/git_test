import requests
import json

url="http://qa.igame.163.com/api/livestream/user/profile/update"
url_get="http://qa.igame.163.com/api/livestream/personalpage/userinfo"
cookie_u='MUSIC_U=baf0583f6bcce48ac15feaaa826ce384d571b19c04b1d5f729ead26780b565e39bffab2f04a1ae7cae2f3fa972ecb108088482c38940710e;os=android'
headers={'content-type':'application/x-www-form-urlencoded','Cookie':cookie_u}
print(headers)
requestData = {'avatarImgId': '109951163393686194'}
res1=requests.post(url,data=requestData,headers=headers)
res2=requests.get(url_get,headers=headers)
print res1.text
print res2.text
