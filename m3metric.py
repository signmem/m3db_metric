#!/bin/bash
# -*- coding:utf-8 -*-
# curl http://10.189.20.63:6203/api/v1/labels

import parameter
import json
import requests
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class M3DB:

    def __init__(self, accessURL, metricName, tagName):
        self.accessURL = accessURL
        self.metricName = metricName
        self.tagName = tagName

    def getM3Lables(self, accessURL, metricName = None, tagName = None):
        """
         param:
         accessURL: 需要自行组合好的 url, 如:
             http://10.189.20.63:6203/api/v1/labels
             http://10.189.20.63:6203/api/v1/label/__name__/values

             返回一个 list, 包含所有 labels
        """
        try:
            allMetricLabelsFromM3 = requests.get(accessURL)
        except Exception as e:
            print("url access false: %s , reason: %s" % (str(accessURL),str(e)))
            return False
        finally:
            try:
                allLabelsJson = json.loads( allMetricLabelsFromM3.text )
            except Exception as e:
                print('not json format: %s , reason: %s' %  (str(accessURL),str(e)))
                return False

        labels = []
        if not allLabelsJson.has_key("data"):
            return labels
        else:
            for i in allLabelsJson["data"]:
                if i == "__name__":
                    pass
                else:
                    labels.append(i)
        return labels

    def getM3Data(self, accessURL, metricName, tagName):
        """

        params:
            accessURL 定义了 query url : http://10.189.20.63:5203/api/v1/query?
            metricName 定义了需要查询的 metricname 如 user_login
            tagName 定义了查询该 metric 是否具有对应的 tag， 如 city

        用于 /api/v1/query
        example:  curl  /api/v1/query?query=user_login{city=~".*"} 
        可以判断出 user_login 是否具有 city, 有返回 True, 没有则返回 False

        """
        queryURL = accessURL + "query=" + metricName + "{" + tagName + '=~".*"}'
        try:
            m3Metric = requests.get(queryURL)
        except Exception as e:
            print("url access false: %s , reason: %s" % (str(accessURL),str(e)))
            return False
        finally:
            try:
                m3MetricJson = json.loads( m3Metric.text )
            except Exception as e:
                print('not json format: %s , reason: %s' %  (str(accessURL),str(e)))
                return False

        if m3MetricJson.has_key("status"):
            if m3MetricJson["status"] == "success":
                if len(m3MetricJson["data"]["result"]) > 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


if __name__ == '__main__':

    # labelurl = "http://" + m3info[0]["url"] + labels_api
    # a = getM3Lables(label)
    # print a

    metricAPI =  parameter.metric_api
    m3info = parameter.m3info
    m3info=[{"namespace":"app","url":"10.189.20.63:6203"}]
    labels_api="/api/v1/labels"
    metric_api="/api/v1/label/__name__/value"
    metricName="redis_connected_clients"
    tagName = "region"
    metricurl = "http://" + m3info[0]["url"] + metric_api
    m3 = M3DB(metricurl, metricName, tagName)
    b = m3.getM3Lables(metricurl)
    print b


    # 判断是否存在某个 tag 的方法
    # metaData_api = "/api/v1/query?"
    # accessURL = "http://" + m3info[0]["url"] + metaData_api
    # metricName = "redis_connected_clients"
    # tagName = "region"
    # m3 = M3DB(accessURL, metricName, tagName)
    # c = m3.getM3Data(accessURL, metricName, tagName)
    # print c
