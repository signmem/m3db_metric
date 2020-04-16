#!/usr/bin/python
# -*- coding:utf-8 -*-

import parameter
import datetime
import time
import os
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


masterDirStamp = datetime.datetime.now().strftime("%Y%m")
dirStamp = datetime.datetime.now().strftime("%Y%m%d")
subDirStamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
pathDir = parameter.savepath

# localPath = pathDir + '/' + masterDirStamp + '/' + dirStamp + '/' + subDirStamp + '/'

localPath = "./m3db"
timeStamp = int(time.time()) - 300


def create_sub_dir():
    """
    dirstamp: parameter.savepath + masterDirStamp +  dirStamp + subDirStamp
                                   yyyymm / yyyymmdd / yyyymmdd_hhmm
    """
    for i in parameter.m3info:
        pdir = i["namespace"]
        isExists = os.path.exists( localPath + '/' +  pdir  )
        if not isExists:
            os.makedirs( localPath + '/' + pdir  )

    return localPath 

