# -*- coding: UTF-8 -*-

import threading
import time
import requests
import json

userid = 478086260
giftId = 285001
batch = 0
num_first = 0
num_second = 0
num_third = 0
thread_num = 50
thread_times = 200
total_times = thread_times*thread_num

if batch == 0:
    batch_here = 1
else:
    batch_here = batch*10



class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        global num_first
        global num_second
        global num_third
        global batch
        global batch_here

        print("Starting " + self.name)

        num_total = thread_times
        while (num_total > 0):
            print(self.name+": "+str(num_total) + " left")
            num_total = num_total - 1
            url = "http://qa-once.igame.163.com/test/api/backend/livestream/lucky/gift/lottery"
            requestData = {'userId': userid, 'giftId': giftId, "batch": batch, "anchorId": 0}
            headers = {'content-type': 'application/x-www-form-urlencoded','Connection':'close'}
            res1 = requests.post(url, data=requestData, headers=headers)
            # print res1.text
            recrestext = res1.text
            recresjson = json.loads(recrestext)
            resdata = recresjson.get('data')
            # print resdata
            if resdata:
                batchGearType = resdata.get('batchGearType')
                gift = resdata.get('giftId')
                lotteryGearType = resdata.get('lotteryGearType')
                if batchGearType != batch_here:
                    print('error batchGearType!!!')
                    break
                if gift != giftId:
                    print('error giftId!!!')
                    break
                if lotteryGearType == 1:
                    threadLock1.acquire()
                    num_first = num_first + 1
                    threadLock1.release()
                elif lotteryGearType == 2:
                    threadLock2.acquire()
                    num_second = num_second + 1
                    threadLock2.release()
                elif lotteryGearType == 3:
                    threadLock3.acquire()
                    num_third = num_third + 1
                    threadLock3.release()
                else:
                    print('other error !!!')
                    break



threadLock1 = threading.Lock()
threadLock2 = threading.Lock()
threadLock3 = threading.Lock()
threads = []
threads_name = []


#创建线程姓名列表
for i in range(thread_num):
    threads_name.append("Thread-"+str(i))


for j in range(thread_num):
    # 创建新线程
    j = myThread(j, threads_name[j])
    # 开启新线程
    j.start()
    # 添加线程到线程列表
    threads.append(j)


# 等待所有线程完成
for t in threads:
    t.join()

print('num_first:',num_first,num_first/total_times)
print('num_second:',num_second,num_second/total_times)
print('num_third:',num_third,num_third/total_times)