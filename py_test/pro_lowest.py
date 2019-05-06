import requests
import json

userid=238591057
giftId=234001
batch=0
num_first=0
num_second=0
num_third=0
num_total=1000
while(num_total>0):
    print num_total
    num_total=num_total-1
    url="http://qa-once.igame.163.com/test/api/backend/livestream/lucky/gift/lottery"
    requestData = {'userId':userid , 'giftId':giftId , "batch": batch,"anchorId":0}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    res1 = requests.post(url, data=requestData, headers=headers)
    #print res1.text
    recrestext=res1.text
    recresjson=json.loads(recrestext)
    resdata=recresjson.get('data')
   # print resdata
    if resdata:
        batchGearType=resdata.get('batchGearType')
        gift=resdata.get('giftId')
        lotteryGearType=resdata.get('lotteryGearType')
        if batchGearType != 1:
            print 'error batchGearType!!!'
            break
        if gift!=giftId:
            print 'error giftId!!!'
            break
        if lotteryGearType==1:
            num_first=num_first+1
        elif lotteryGearType==2:
            num_second=num_second+1
        elif lotteryGearType==3:
            num_third=num_third+1
        else:
            print 'other error !!!'
            break


print ('num_first:',num_first)
print ('num_second:',num_second)
print ('num_third:',num_third)