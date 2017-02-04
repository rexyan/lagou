#--*--coding:utf-8--*--
from Config import SQL_Helper

'分布式进程 -- 服务器端'
import random, multiprocessing
from multiprocessing.managers import BaseManager
from multiprocessing import freeze_support
import time
from Template import GetJobName
import sys


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 发送任务的队列:
task_queue = multiprocessing.Queue()
# 接收结果的队列:
result_queue = multiprocessing.Queue()

# 为解决__main__.<lambda> not found问题
def get_task_queue():
    return task_queue

# 为解决__main__.<lambda> not found问题
def get_result_queue():
    return result_queue


# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=get_task_queue)
QueueManager.register('get_result_queue', callable=get_result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('127.0.0.1', 5000), authkey=b'abc')


def communicate(FirstCategory):
    # 获得通过网络访问的Queue对象:
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    #从数据库查询职位列表，非配任务
    Assign_task(task,FirstCategory)

    # 从result队列读取结果:
    Get_back_data(result)

    # 关闭:
    manager.shutdown()


def Assign_task(task,FirstCategory):
    # 从数据库查询职位列表，非配任务

    sql = "select TypeSearchName from home_jobtype WHERE  FirstCategory='%s'"%(FirstCategory)
    re = SQL_Helper.Select_fetchall(sql)
    print(len(re))

    if len(re) > 0:
        print(u"共获取%s个职位标签,正在分配爬取任务" % ((len(re))))
        for i in range(len(re)):
            print('分配职位标签: %s...' % re[i])
            task.put(re[i])
    else:
        print(u"没有获取到职位标签！")
    print(u'任务分配完毕')


def Get_back_data(result):
    # 从result队列读取结果:
    print('正在尝试获取数据...')
    tag=True
    i=1
    while tag:
        if result.empty():
            print (u'等待客户端返回值，10秒后重试...')
            time.sleep(10)
            i=i+1
            if i > 50:
                tag=False
                print ('任务结束')

        else:
            print (u'提示：检测到客户端正在回传数据，正在确认完成性')
            tmp_size =result.qsize()

            for i in range(result.qsize()):
                r = result.get(timeout=1)
                if r=="over":
                    break
                else:
                    print ("提示:接收到返回数据,准备清洗保存...返回有效数据个数为:%d"%len(r))
                    #保存
                    for x in r:
                        try:
                            #print(x)
                            nowdate = (time.strftime('%Y-%m-%d') + "-" + x['time']).replace(("发布"),"")
                            #保存到招聘职位表
                            sql = "insert into home_position(Id,JobName,Salary,CompanyName,Time,CompanyWebsite) VALUES(%d,%s,%s,%s,%s,%s);"%(int(x["id"]),"'"+x["jobname"]+"'","'"+x["salary"]+"'","'"+x["companyname"]+"'","'"+nowdate+"'","'"+x["companywebsite"]+"'")
                            re,lastid = SQL_Helper.Insert_data(sql)
                            PositionID=lastid

                            #数据保存到职位基本要求表
                            #拆分地址
                            for t in range(len(x['jobbaserequirement'].split('/'))):
                                sql1 = "insert into home_jobbaserequirement(PositionID,Education,Experience) VALUES (%d,%s,%s);"%(int(PositionID),"'"+(x['jobbaserequirement'].split('/'))[0]+"'","'"+(x['jobbaserequirement'].split('/'))[1]+"'")
                                SQL_Helper.Insert_data(sql1)
                                #print(sql1)

                            #保存tag
                            tag=x["tag"].replace("\n", "")
                            sql2 = "insert into home_tag(PositionID,JobTag) VALUES (%d,%s);" %(int(PositionID), "'" +tag+ "'")
                            #print(sql2)
                            SQL_Helper.Insert_data(sql2)

                            #职位诱惑表
                            sql3 = "insert into home_welfare(PositionID,JobWelfare) VALUES (%d,%s);" %(int(PositionID), "'" + x["welfare"] + "'")
                            #print(sql3)
                            SQL_Helper.Insert_data(sql3)

                            #招聘职位详情表
                            sql4= "insert into home_detailsrecruitment(PositionID,CompanyID,DescriptionRequirements,Address,Person,PersonPosition) VALUES (%d,%d,%s,%s,%s,%s);" % (int(PositionID), int(x["DetailsPageData"]["companyid"]),"'"+x["DetailsPageData"]["Requirement"]+"'","'"+x["DetailsPageData"]["add"]+"'","'"+x["DetailsPageData"]["person"]+"'","'"+x["DetailsPageData"]["posi"]+"'")
                            #print(sql4)
                            SQL_Helper.Insert_data(sql4)

                            #公司表：
                            print("信息长度",len(x["DetailsPageData"]["info"]))
                            CompanyType = x["DetailsPageData"]["info"][0]           #类型
                            CompanyDevelopment=x["DetailsPageData"]["info"][1]      #发展

                            if len(x["DetailsPageData"]["info"])==4:
                                CompanyWebSite = str(x["DetailsPageData"]["info"][3]).replace(("公司主页"),"")
                                CompanyScale=x["DetailsPageData"]["info"][2]
                                CompanyInvestment="无"

                            elif len(x["DetailsPageData"]["info"])==5:
                                CompanyWebSite = str(x["DetailsPageData"]["info"][4]).replace(("公司主页"),"")     #官网
                                CompanyInvestment=x["DetailsPageData"]["info"][2]    #投资
                                CompanyScale=x["DetailsPageData"]["info"][3]         #规模

                            sql5= "insert into home_company(CompanyID,CompanyName,CompanyType,CompanyAdd,CompanyDevelopment,CompanyWebSite,CompanyLogo,PositionID,JobName,addtime,CompanyInvestment,CompanyScale) VALUES (%d,%s,%s,%s,%s,%s,%s,%d,%s,%s,%s,%s);"%(int(x["DetailsPageData"]["companyid"]),"'"+x["DetailsPageData"]["name"]+"'","'"+CompanyType+"'","'"+x["DetailsPageData"]["add"]+"'","'"+CompanyDevelopment+"'","'"+CompanyWebSite+"'","'"+x["DetailsPageData"]["img"]+"'",int(PositionID),"'"+x["jobname"]+"'","'"+nowdate+"'","'"+CompanyInvestment+"'","'"+CompanyScale+"'")
                            #print(sql5)
                            SQL_Helper.Insert_data(sql5)

                            #城市表
                            add=str(x["DetailsPageData"]["add"]).split("-")
                            if len(add)>1:
                                CityFirstName=add[0]
                                CitySecondName=add[1]
                                OtherName=x["DetailsPageData"]["add"]
                                CompanyId=int(x["DetailsPageData"]["companyid"])
                                sql6 = "insert into home_city(CityFirstName,CitySecondName,OtherName,CompanyId) VALUES (%s,%s,%s,%d);" % ("'"+CityFirstName+"'","'"+CitySecondName+"'","'"+OtherName+"'",CompanyId)
                                #print(sql6)
                                SQL_Helper.Insert_data(sql6)
                        except Exception as e:
                            content="\n"+str(time.strftime('%Y-%m-%d %H:%i:%m'))+"::::::"+e
                            print("出现错误，记录日志")
                            f = open('Runlog.txt', 'ab')
                            f.write(content)
                            f.close()

                tag = False

def main(FirstCategory):
    freeze_support()
    # 启动Queue:
    manager.start()
    communicate(FirstCategory)

if __name__=='__main__':
    begintype = sys.argv[1]
    main(begintype)