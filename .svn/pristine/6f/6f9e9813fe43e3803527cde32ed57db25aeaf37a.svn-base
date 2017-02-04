#--*--coding:utf-8--*--

import time, sys, queue
from multiprocessing.managers import BaseManager
from Template import GetListData
import threading,time
from time import sleep, ctime
import queue
result = queue.Queue()

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')




#连接服务器
def Connect_Server():
    try:
        # 连接到服务器，也就是运行taskmanager.py的机器:
        server_addr = '127.0.0.1'
        print('正在连接到服务器 %s...' % server_addr)
        # 端口和验证码注意保持与taskmanager.py设置的完全一致:
        m = QueueManager(address=(server_addr, 5000), authkey=b'abc')
        # 从网络连接:
        m.connect()
        print (u'连接服务器成功,正在获取本次爬取任务...')
        # 获取Queue的对象:
        task = m.get_task_queue()
        result = m.get_result_queue()
        return task,result
    except  Exception as e:
        print (e)

#判断是否有任务，并获取完成的任务
def Is_Completed():
    tag=True
    while tag:
        if task.qsize()==0:
            print (u'无任务，3秒后重试...')
            time.sleep(3)
        else:
            task_num=task.qsize()
            time.sleep(5)
            if task.qsize()==task_num:
                print (u'获取到完成的任务列表')
                break
            else:
                print(u'获取到任务列表，任务列表不完整')
                Is_Completed()
            break

def Acquisition_task():   #获取任务
    tasklist=[]
    for i in range(task.qsize()):
        try:
            n = task.get(timeout=1)
            print('获取到职位标签:%s...' % (n))
            tasklist.append(n[0])
        except queue.Empty:
            print('空队列')

    #print (tasklist)

    thlist=[]
    print ("多线程开始")
    for x in range(len(tasklist)):
        print (tasklist[x])
        th=threading.Thread(target=GetListData.main,args=(tasklist[x],30,))
        thlist.append(th)

    for th in thlist:
        th.start()

    for th in thlist:
        th.join()

    print("主进程等待子线程结束")
    while not GetListData.result.empty():
        print("收到子线程传回数据:")
        returndata=GetListData.result.get()
        print(returndata)
        result.put(returndata)  # 把结果写入result队列:
    result.put("over")

    # for i in range(task.qsize()):
    #     try:
    #         n = task.get(timeout=1)
    #
    #         print('获取到职位标签:%s...' % (n))
    #         print('正在开始爬取%s' %(n))
    #
    #         #开始
    #         print (n[0])  #打印即将开始的job name，防止出错
    #         returndata = GetListData.main(n[0], 30)
    #         print ('+++++++++++控制提醒，收到数据+++++++++++')
    #         print(returndata) #打印返回的数据，防止出错
    #         #结束
    #         result.put(returndata)    #把结果写入result队列:
    #
    #     except queue.Empty:
    #         print('空队列')
    # 处理结束:
    print('任务结束')


if __name__=='__main__':
    tag=True
    while tag:
        try:
            task,result=Connect_Server()
            Is_Completed()
            Acquisition_task()
            print("10s监测任务")
            time.sleep(10)
        except Exception:
            print("服务器连接失败,开始60s监测任务")
            time.sleep(60)




