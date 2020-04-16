#!/usr/bin/python
#  -*- coding:utf-8 -*-

import mysqlUtils
import parameter
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


host = parameter.db["host"]
password = parameter.db["password"]
user = parameter.db["user"]
dbname = parameter.db["dbname"]

mysql = mysqlUtils.MySQL(host, user, password, dbname)

class DBControll():

    def getNameSpaceID(self, nameSpace):
        """
        params:
           nameSapce: 输入 namespace 
           return namespace ID
        """
        checkSQL = "select id from m3db_namespace where name = '" + nameSpace + "'"
        try:
            nameSpaceID = mysql.get_one(checkSQL)
        except Exception as e:
            print("check namespace: %s false" % nameSapce)
            return 0
        finally: 
            if nameSpaceID is None or len(nameSpaceID) == 0:
                insertSQL = "insert into m3db_namespace (name) values ('" + nameSpace  + "');"
                try:
                    nameSpaceIns = mysql.insert(insertSQL)
                except:
                    print("insert namespace: %s false" % (nameSpace))
                    return 0
                finally:
                    nameSpaceID = mysql.get_one(checkSQL)
                    return nameSpaceID[0]
            else:
                return nameSpaceID[0]

    def checkID(self, nameSpace, tableName, columnName):
        """
        params:
            tagName: 对应  m3metric.m3db_tag 中 tagname 列
            检查是否存在， 不存在则插入
            return: 插入成功或存在都返回 tag ID, 错误返回 0
        """
        nameSpaceID = self.getNameSpaceID(nameSpace)
        checkSQL = "select id from " + tableName  + " where name = '" + columnName + "' and namespace_id='" + str(nameSpaceID) + "'"
        try:
            columnID = mysql.get_one(checkSQL)
        except Exception as e:
            print("check table: %s , column %s false" % (tableName, columnName))
            return 0
        finally:
            if columnID is None or len(columnID) == 0:
                insertSQL = "insert into " + tableName + " (name, namespace_id) values ('" + columnName  + "','" + str(nameSpaceID) + "')"
                # print insertSQL
                try:
                   columnIns = mysql.insert(insertSQL)
                except:
                    print("insert table: %s, column %s false" % (tableName, columnName))
                    return 0
                finally:
                    columnID =  mysql.get_one(checkSQL)
                    return columnID[0]
            else:
                return columnID[0]

    def checkMetricTag(self, nameSpace, metricName, tagName):
        """
        params:
           metricName:
           tagName:
           检查 metricName 与 tagName 是否已经在表 m3db_tag_mapping 已建立关系
           关系存在返回 metricID, 不存在则建立关系
           return 返回 metricID, 只需要判断返回 > 0 不为 None 则可
        """
        tagID = self.checkID(nameSpace, "m3db_tag", tagName)
        metricID = self.checkID(nameSpace, "m3db_metric",  metricName)

        checkSQL = "select metric_id from m3db_tag_mapping where metric_id = '" + str(metricID) + "' and tag_id = '" + str(tagID) + "'"
        try:
            mappingID = mysql.get_one(checkSQL)
        except Exception as e:
            print("check metric %s , tag %s mapping false" % (metricName, tagName))
            return 0
        finally:
            if mappingID is None or len(mappingID) == 0:
                insertSQL = "insert into m3db_tag_mapping (metric_id, tag_id) values ('" + str(metricID) + "','" + str(tagID) + "')"
                try:
                    mappingIns = mysql.insert(insertSQL)
                except:
                    print("insert  metric %s , tag %s mapping false" % (metricName, tagName))
                    return 0
                finally:
                    mappingID = mysql.get_one(checkSQL)
                    return mappingID[0]
            else :
                return mappingID[0]


if __name__ == '__main__':

    nameSpace = "app"
    metricName = "abc"
    tableName = "m3db_tag"
    #tableName = "m3db_namespace"
    columnData = "app1s"
    columnData = "c3d22"
    db = DBControll()
    metricName = "terr22y22"
    b = db.checkMetricTag(nameSpace, metricName, columnData)
    print b

