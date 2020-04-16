#!/usr/bin/python
# -*- coding:utf-8 -*-

import parameter
import m3metric
import toolUtils
import metricToDB
import json
import re
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def main():

    # localPath = toolUtils.create_sub_dir()

    labelAPI =  parameter.label_api
    metricAPI = parameter.metric_api
    queryAPI =  parameter.query_api


    m3info = parameter.m3info

    for m3list in m3info:
        nameSpace = m3list["namespace"]
        apiURL = m3list["apiURL"]
        queryURL = m3list["queryURL"] + queryAPI

        tagURL = apiURL + labelAPI    # get all tagName 
        metricURL = apiURL + metricAPI  # get all metric name (__name__)

        targeName = None
        metricName = None
        m3 = m3metric.M3DB(tagURL, metricName, targeName)

        # 获得所有的 tag name
        tagTotal = m3.getM3Lables(tagURL)

        # 获得所有的 metric name  
        metricTotal = m3.getM3Lables(metricURL)

        #  写入本地文件测试 开始
        #metricFile = localPath + '/' + nameSpace + '_metric'
        #tagFile = localPath + '/' + nameSpace + "_tags"
        #with open(metricFile, 'w') as f:
        #    json.dump(metricTotal, f)
        #with open(tagFile, 'w') as t:
        #    json.dump(tagTotal, t)
        #  写入本地文件测试 结束


        for metricName in metricTotal:

            if re.match("^\d", metricName) or re.search("\.", metricName) or re.search("unknown", metricName):
                continue

            #  写入本地文件测试
            # print metricName
            # metricTagFile = localPath + '/' + nameSpace + '/' + metricName 

            metricTags = {}
            metricTags["name"] = metricName
            tags = []

            for tagName in tagTotal:

                if re.match("^\d", tagName) or re.search("\.", tagName):
                    continue

                status = m3.getM3Data(queryURL, metricName, tagName)

                if status:
                   checkDB = metricToDB.DBControll()
                   # print("namespace: %s  metricName: %s tagName: %s" % (nameSpace, metricName, tagName))
                   metricID = checkDB.checkMetricTag( nameSpace, metricName, tagName)

                   if metricID == 0 or metricID is None:
                       print ("namespace: %s  metricName: %s tagName: %s" % (nameSpace, metricName, tagName))
                       break
                else:
                    break

            #  写入本地文件测试 开始
            #    if status:
            #        tags.append(tagName)
            #     metricTags["tagName"] = tags
            # with open(metricTagFile, 'w') as file_object:
            #    json.dump(metricTags, file_object)
            #  写入本地文件测试 结束

if __name__ == '__main__':

    main()

