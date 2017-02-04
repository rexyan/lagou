from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib
import urllib.request
from Config import SQL_Helper

def GetJobName(url):
    html = urlopen(url)
    obj = BeautifulSoup(html.read())
    data = obj.findAll("div", {"class": {"mainNavs"}})

    if len(data)>0:
        for x in data:
            menu_box=x.findAll("div", {"class": {"menu_box"}})
            for s in menu_box:
                name=s.findAll("div", {"class": {"menu_main","job_hopping"}})
                for x in name:
                    FirstCategory=x.h2.get_text().strip()   #一级栏目名称
                    print("--一级栏目名称",FirstCategory)

                    menu_sub_dn=s.findAll("div",{"class":{"menu_sub","dn"}})
                    for d in menu_sub_dn:
                        dl=d.findAll('dl')
                        for t in dl:
                            dt=t.findAll("dt")
                            for aa in dt:
                                a=aa.findAll("a")
                                SecendCategory=(a[0].get_text())  #二级栏目名称
                                print("------二级栏目名称",SecendCategory)

                            dd = t.findAll("dd")
                            for dda in dd:
                                a = dda.findAll("a")
                                for x in range(len(a)):
                                    print ("------------三级栏目名称",a[x].get_text())
                                    url=(str(a[x]['href'])).split("//")[1]
                                    url2=url.split("/")
                                    leng=len(url2)
                                    print("----------------------搜索关键字",url2[2])


                                    #判断是否存在JobName数据，存在则不管，不存在则增加
                                    sql = "select FirstCategory from home_jobtype WHERE TypeSearchName=%s and TypeDisPlayname=%s;"%("'"+url2[2]+"'","'"+a[x].get_text()+"'")
                                    searchre = SQL_Helper.Select_fetchall(sql)
                                    if (len(searchre))==0:
                                        sql = "insert INTO home_jobtype(FirstCategory,SecendCategory,TypeSearchName,TypeDisPlayname) VALUES (%s,%s,%s,%s);" %("'"+FirstCategory+"'","'"+SecendCategory+"'","'"+url2[2]+"'","'"+a[x].get_text()+"'")
                                        #print(sql)
                                        re = SQL_Helper.Insert_data(sql)
                                    else:
                                        pass
def main(url):
    GetJobName(url)






