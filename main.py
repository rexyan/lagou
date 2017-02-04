#--*--coding:utf-8--*--
import time
import os
import logging
import subprocess
import sys
from Config import SQL_Helper
from Template import GetJobName,Email



if __name__=='__main__':
    print("脚本启动，检查时间中...")
    today_iscom={"status":False,"time":"0"}

    while True:
        today = (time.strftime('%Y-%m-%d'))
        time1 = (time.strftime('%H:%m'))
        h = str(time1).split(":")[0]
        m = str(time1).split(":")[1]
        print("今天日期%s,当前时间:%s"%(today,str(time1)))

        if (int(h)>=22 and today_iscom['status']==False):     #判断是否开始今日任务
            begintime=(time.strftime('%H:%m'))                #任务开始时间
            GetJobName.main("https://www.lagou.com/")
            print("抓取存储完毕,开始按照类别分配任务")
            sql = "select DISTINCT FirstCategory from home_jobtype;"
            re = SQL_Helper.Select_fetchall(sql)
            #循环调用Server端
            for s in range(len(re)):
                jobtype=re[s][0]
                print("工作类型:",jobtype)
                os.system("py -3 Server.py %s"%(jobtype))
            print("今日任务完毕,准备发送邮件中...")
            today_iscom['status']=True
            comtime=(time.strftime('%H:%m'))                 #任务结束时间

            #发送邮件，汇总今日抓取情况
            likeguanjainzi = "'""%" + today + "%""'"
            sql = "select count(*) from home_position where Time like %s;" % (likeguanjainzi)  # 聘职位信息数量
            re = SQL_Helper.Select_fetchall(sql)
            sql = "select count(*) from home_position;"  # 聘职位信息总数
            re1 = SQL_Helper.Select_fetchall(sql)
            sql = "select count(*) from home_company where addtime like %s;" % (likeguanjainzi)  # 今日公司数量
            re2 = SQL_Helper.Select_fetchall(sql)
            sql = "select count(*) from home_company;"  # 公司总数量
            re4 = SQL_Helper.Select_fetchall(sql)
            sql = "select count(*) from home_welfare;"  # 公司福利表
            re5 = SQL_Helper.Select_fetchall(sql)
            sql = "select count(*) from home_tag;"  # 公司Tag
            re6 = SQL_Helper.Select_fetchall(sql)

            Email.sendmail(today + "抓取任务结束" + "\n" + "任务开始时间:" + "" + begintime + "" + "\n" + "任务结束时间:" + comtime + "" + "\n" + "今日获取招聘职位信息数量:" + str(
                    re[0][0]) + ",目前职位信息数量总和:" + "" + str(re1[0][0]) + "\n" + "今日获取招聘职位公司数目:" + str(
                    re2[0][0]) + ",目前招聘职位公司总和:" + str(re4[0][0]) + "\n" + "公司福利条目总和:" + str(
                    re5[0][0]) + "\n" + "Tag条目总和:" + str(re6[0][0]) + "")

        else:
            print("非抓取时间,一小时后检测")
            time.sleep(3600)
            # 检查是否为第二天
            if (today==(time.strftime('%Y-%m-%d')) and today_iscom['status']==True):
                today_iscom['status'] = True      #还是今天，并且任务已经完成
            else:
                today_iscom['status'] = False     #是第二天，并且任务没有完成




