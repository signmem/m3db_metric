#!/usr/bin/python
# -*- coding:utf-8 -*-

import pymysql
import parameter
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class MySQL():
    def __init__(self, host, user, passwd, dbName):
        self.host =host
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
    
    def connect(self):
        self.db = pymysql.connect(self.host, self.user, self.passwd, self.dbName)
        self.cursor = self.db.cursor()
        
    def close(self):
        self.cursor.close()
        self.db.close()
    
    def get_one(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print("select from db faile :" + str(e))
            return False
        return res
    
    def get_all(self, sql):
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print("select from db faile :" + str(e))
            return False
        return res
    
    def insert(self,sql):
        return self.__edit(sql)
            
    def update(self,sql):
        return self.__edit(sql)
            
    def delete(self,sql):
        return self.__edit(sql)
            
    def ddl(self, sql):
        return self.__edit(sql)

    def __edit(self,sql):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except Exception as e:
            self.db.rollback()
            print('transtion false :' + str(e))
            return False
        return count 

if __name__ == '__main__':

    dbinfo = {"host":"localhost","user":"terry","password":"terry.123", "dbname":"m3metric"}
    host = dbinfo["host"]
    user = dbinfo["user"]
    password = dbinfo["password"]
    dbname = dbinfo["dbname"]
    db= MySQL(host, user, password, dbname)
    tablename = "m3db_namespace"
    SQL = "select * from " +  dbname + "." + tablename
    info = db.get_all(SQL)
    if info != False:
        print info
    tagname = "app"
    SQL = "insert into m3db_tag (tagname) values ('" + tagname + "')"
    info = db.insert(SQL)
    if info != False:
        print info

