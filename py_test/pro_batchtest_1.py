# coding=utf-8
from __future__ import division
import threading
import time
import requests
import json


userid=478086262
giftId=285001
batch=1
num_first=0
num_second=0
num_third=0
times=100000
num_total=times

lock1 = threading.RLock()
lock2 = threading.RLock()
lock3 = threading.RLock()
lock4 = threading.RLock()

def Func():
    #lock.acquire()
    global num_total
    global num_first
    global num_second
    global num_third
    while(num_total>0):
        lock4.acquire()
        print num_total
        num_total=num_total-1
        lock4.release()
        url="http://qa-once.igame.163.com/test/api/backend/livestream/lucky/gift/lottery"
        requestData = {'userId':userid , 'giftId':giftId , "batch": batch,"anchorId":0}
        headers = {'content-type': 'application/x-www-form-urlencoded','Connection':'close'}
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
            if batchGearType != 10:
                print 'error batchGearType!!!'
                break
            if gift!=giftId:
                print 'error giftId!!!'
                break
            if lotteryGearType==1:
                lock1.acquire()
                num_first=num_first+1
                lock1.release()
            elif lotteryGearType==2:
                lock2.acquire()
                num_second=num_second+1
                lock2.release()
            elif lotteryGearType==3:
                lock3.acquire()
                num_third=num_third+1
                lock3.release()
            else:
                print 'other error !!!'
                break
         #   print ('num_first:',num_first)
         #   print ('num_second:',num_second)
         #   print ('num_third:',num_third)


start_time = time.time()
thread_list = []
for i in range(50):
    t = threading.Thread(target=Func)
    thread_list.append(t)

for t in thread_list:
    t.setDaemon(True)
    t.start()

for t in thread_list:
    t.join()

print ('num_first:',num_first,num_first/times)
print ('num_second:',num_second,num_second/times)
print ('num_third:',num_third,num_third/times)
print('total time：', time.time()-start_time)
