#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @连接数据库操作
import pymysql.cursors
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '18525350524Yrs',
    'db': 'neu',
    'charset': 'utf8',
}

# @函数名 : Select_fetchall
# @函数功能描述 :数据库查询
# @函数参数 :sql：string
# @函数返回值 : 返回查询到的数据,tuple格式
def Select_fetchall(sql):
    connect = pymysql.connect(**config)
    try:
        with connect.cursor() as cursor:
            cursor.execute(sql);
            result = cursor.fetchall();
            return result
    finally:
        connect.close();


# @函数名 : Insert_data
# @函数功能描述 :数据库插入或者删除
# @函数参数 :sql：string
# @函数返回值 : 返回查询到的插入成功的数据条数
def Insert_data(sql):
    connect = pymysql.connect(**config)
    try:
        with connect.cursor() as cursor:
            cursor.execute(sql);
            result = connect.commit()
            return result,cursor.lastrowid
    finally:
        connect.close();

