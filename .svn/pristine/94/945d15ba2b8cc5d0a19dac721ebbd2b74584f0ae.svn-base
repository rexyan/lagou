# --*-- coding:utf-8 --*--

# @Author  : Rex
# @Site    :
# @File    : GetListData.py
# @Software: PyCharm
# 传入job name 抓取当天的job发布信息


from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import urllib.request
import queue
result = queue.Queue()


# @函数名 : MosaicUrl
# @函数功能描述 :拼接URL
# @函数参数 : job_name:string,page:string
# @函数返回值 : 返回拼接好的URL
def MosaicUrl(job_name,page):
     url="https://www.lagou.com/zhaopin/"+job_name+"/"+page+"/?filterOption=2"
     print ('即将开始:',url)
     return  url


# @函数名 : Begin
# @函数功能描述 :抓取内容
# @函数参数 : job_name:string,page:string
# @函数返回值 : 返回新数据,dict格式
def Begin(job_name,page):
    url=MosaicUrl(job_name,page)
    try:
       html=urlopen(url)
       obj=BeautifulSoup(html.read())
       data=obj.findAll("ul",{"class":{"item_con_list"}})
       if len(data)==0:
           print ('获取内容为空')
       else:
           li=obj.findAll("li",{"class":{"con_list_item","default_list"}})
           for x in li:
               time=x.find("span",{"class":{"format-time"}})  #获取时间
               if ((time.get_text()).find('前')>0 or (time.get_text()).find('-')>0):
                   print('发现过期数据',time.get_text())
                   break
               else:
                   try:
                        #赋值
                        id=x['data-companyid']
                        jobname= x['data-positionname']
                        salary=(x.find("span",{"class":{"money"}})).get_text()
                        companyname=x['data-company']
                        companywebsite=(x.find("a",{"class":{"position_link"}})['href']).split('//')[1].strip()
                        workadd=(x.find("span",{"class":{"add"}})).find("em").get_text()
                        time=time.get_text()
                        jobbaserequirement=(((x.find("div",{"class":{"li_b_l"}})).get_text()).split("经验")[1])
                        tag=(x.find('div',{"class":{"list_item_bot"}})).find("div",{"class":{"li_b_l"}}).get_text()
                        welfare=x.find('div',{"class":{"li_b_r"}}).get_text()

                        #打印调试
                        print(
                            "公司ID:", id,
                            "招聘职位名称:", jobname,
                            "工资:", salary,
                            "公司名称:", companyname,
                            "公司招聘该职位的主页:", companywebsite,
                            "职位工作地址:", workadd,
                            "发布时间:", time,
                            "职位基本要求:", jobbaserequirement,
                            "职位tag:", tag,
                            "职位诱惑:", welfare
                        )

                        print("\n开始抓取%s招聘%s的详细信息\n"%(companyname,jobname))
                        re=BeginDetailsPage(companywebsite)
                        print("\n抓取完毕，获取到抓取结果，准备合并数据返回...\n",re)




                        dictname={"id":id,
                               "jobname":jobname,
                               "salary":salary,
                               "companyname":companyname,
                               "companywebsite":companywebsite,
                               "workadd":workadd,
                               "time":time,
                               "jobbaserequirement":jobbaserequirement,
                               "tag":tag,
                               "welfare":welfare,
                               "DetailsPageData":re
                               }
                        return dictname

                   except Exception as e:
                        print("分析出现错误2",e)
                        break

    except Exception as e:
        print("分析出现错误1", e)




def BeginDetailsPage(url):
    data={"Requirement":"","add":"","companyid":"","name":"","info":"","img":"","person":"","posi":""}
    url="https://"+url
    #print (url)
    html = urlopen(url)
    obj = BeautifulSoup(html.read())

    #招聘要求
    dd = obj.findAll("dd", {"class": {"job_bt"}})
    if len(dd)>0:
        for x in dd:
            Requirement=(str(x.findAll('p')).replace("</p>,","").replace(("<br/>"),"").replace(("</br>"),""))
            #print ("招聘要求",Requirement)
            data["Requirement"]=Requirement

    #工作地址
    wordadd=obj.findAll("div",{"class":{"work_addr"}})
    if len(wordadd) >0:
        for s in wordadd:
            add=(s.get_text()).replace((" "),"").replace(("\n"),"").replace(("查看地图"),"")
            #print ("工作详细地址",add)
            data["add"]=add

    #公司Id
    companyid = obj.findAll("div", {"class": {"position-head"}})
    if len(companyid)>0:
        for x in companyid:
            #print ("公司ID",x["data-companyid"])
            data["companyid"]=x["data-companyid"]

    #公司名称
    companyname=obj.findAll('dl',{"id":{"job_company"}})
    if len(companyname)>0:
        for x in companyname:
            companypage=x.findAll("h2",{"class":{"fl"}})
            for x in companypage:
                name=x.get_text().replace(("拉勾认证企业"),"").replace(("\n"),"").replace((" "),"")
                #print ("公司名称",name)
                data["name"]=name

    #公司基本信息
    infomation=[]
    companyinfo=obj.findAll("ul",{"class":{"c_feature"}})
    if len(companyinfo)>0:
        for x in companyinfo:
            li=x.findAll("li")
            for ii in li:
                info=ii.get_text().replace(("\n"),"").replace((" "),"").replace(("<br>"),"")
                infomation.append(info)
        data["info"]=infomation
                #print ("公司类型，工地发展阶段，投资情况，人数规模，公司官网",ii.get_text().replace(("\n"),"").replace((" "),"").replace(("<br>"),""))

    #公司LOGO
    logo=obj.findAll("img",{"class":{"b2"}})
    if len(logo)>0:
        for x in logo:
            img=str(x["src"]).split("//")[1]
            #print ("公司LOGO",img)
            data['img']=img


    #公司招聘人
    hr=obj.findAll("input",{"class":{"hr_name"}})
    if len(hr)>0:
        for x in hr:
            person=x["value"]
            #print ("招聘人",person)
            data["person"]=person

    #公司招聘人职位
    hr1=obj.findAll("input",{"class":{"hr_position"}})
    if len(hr1)>0:
        for x in hr1:
            posi=x["value"]
            #print ("职位",posi)
            data["posi"]=posi

    return (data)

# @函数名 : main
# @函数功能描述 :主程序
# @函数参数 :job_name：string，page：int
# @函数返回值 : 返回抓取到的数据,list格式
def main(job_name,page):
    data1 = []
    for x in range(page):    #页数
        print("****即将开始第%s页****"%str(x+1))
        data="redata" + str(x + 1)
        data=Begin(str(job_name),str(x+1))
        if data!=None:
            data1.append(data)
    print("\n类型列表任务完成,返回数据\n", data1)
    if len(data1)>0:
        result.put(data1)
    return data1












