# coding: utf-8
# -*- coding = utf-8 -*-
#!e:/code/python
# psyco.full()

'''
Created on 2013-5-6

@author: Administrator
'''

from __future__ import division
from openpyxl import Workbook
from datetime import datetime
import math
import xlrd

log10 = math.log10
log = math.log

def normalizeList(l, per=0.05 , enlar=1e2):
    N = len(l)
    l[1] = logData(l[1])
    l[2] = logData(l[2])
    l[3] = logData(l[3])
    l[4] = logData(l[4])
    for i in range(N):
        normalize(l[i], per, enlar)
    return l

def normalizeListCom(l, per=0.05 , enlar=1e2):
    N = len(l)
    for i in range(N):
        normalize(l[i], per, enlar)
    return l

def normalize(data, per=0.05 , enlar=1e2):
    max_data = max(data)
    min_data = min(data)
    percent = (max_data - min_data) * per
#    tmp = 0.05
    for i in range(len(data)):
        tmp = data[i]
        data[i] = (tmp - min_data + percent) / (max_data - min_data + percent) * enlar
    return data

def logData(data):
    for i in range(len(data)):
        tmp = data[i]
        if tmp == 'NaN':
            tmp = 0
        if tmp != 0:
            data[i] = log(tmp + 1)
    return data

def getColData(table, colIndex=0, beginRow=0):
    col = table.col_values(colIndex)
    return col[beginRow:]

def getRequiredData(f=r'/2013-4-23/nmgw.xlsx', indexList=[3, 4, 7, 8]):
    book = xlrd.open_workbook(f)
    table = book.sheets()[0]
    result = []
    for i in indexList:
        result.append(getColData(table, i, 1))
    return result
    
def writeNData(dataList, f=r'/5-5/new_norm_mgw.xlsx'):
    start = datetime.now()
    wb = Workbook(optimized_write=True);
    ws = wb.create_sheet(0, 'sheet1')
    cols = len(dataList)
    rows = len(dataList[0])
#    ws.append(['ExcelID', '归一化发布时间', '归一化粉丝数', '归一化转发数', '归一化评论数', '归一化url', '归一化TF-IDF', '原始发布时间', '原始粉丝数', '原始转发数', '原始评论数', '原始url', '原始TF-IDF'])
#    for j in range(1, cols):
#        print j, sum(dataList[j]) / rows
    for i in range(rows):
#        writeRow = [i + 2]
        writeRow = []
        for j in range(cols):
            writeRow.append(dataList[j][i])
        ws.append(writeRow)
    wb.save(f)
    print '写入 %s 花了 %d 秒' % (f, (datetime.now() - start).seconds)

def cope(rf, wf):
    print '处理%s开始' % rf
    odata = getRequiredData(rf, [2, 3, 4, 5, 6 , 7])
    ndata = []
    for i in range(len(odata)):
        ndata.append(list(odata[i]))
    ndata = normalizeList(ndata)
    todata = ndata
    writeNData(todata, wf)
    print '处理%s结束' % rf

if __name__ == '__main__':
    print 'begin'
    fold = u'./complete'
    n = 8
    readfile = [u'/tfidfExcel/2013两会tfidf.xlsx', u'/tfidfExcel/H7N9tfidf.xlsx', u'/tfidfExcel/北京雾霭天气tfidf.xlsx',
      u'/tfidfExcel/第一夫人彭丽媛tfidf.xlsx', u'/tfidfExcel/国五条tfidf.xlsx', u'/tfidfExcel/黄浦江死猪tfidf.xlsx',
      u'/tfidfExcel/撒切尔夫人tfidf.xlsx', u'/tfidfExcel/雅安地震tfidf.xlsx']
    writefile = [u'/normExcel/2013两会norm.xlsx', u'/normExcel/H7N9norm.xlsx', u'/normExcel/北京雾霭天气norm.xlsx',
      u'/normExcel/第一夫人彭丽媛norm.xlsx', u'/normExcel/国五条norm.xlsx', u'/normExcel/黄浦江死猪norm.xlsx',
      u'/normExcel/撒切尔夫人norm.xlsx', u'/normExcel/雅安地震norm.xlsx']
#    readfile = [u'/tfidfExcel/2013两会alltfidf.xlsx', u'/tfidfExcel/H7N9alltfidf.xlsx', u'/tfidfExcel/北京雾霭天气1alltfidf.xlsx',
#      u'/tfidfExcel/第一夫人彭丽媛alltfidf.xlsx', u'/tfidfExcel/国五条alltfidf.xlsx', u'/tfidfExcel/黄浦江死猪alltfidf.xlsx',
#      u'/tfidfExcel/撒切尔夫人alltfidf.xlsx', u'/tfidfExcel/雅安地震alltfidf.xlsx']
#    writefile = [u'/normExcel/2013两会allnorm.xlsx', u'/normExcel/H7N9allnorm.xlsx', u'/normExcel/北京雾霭天气1allnorm.xlsx',
#      u'/normExcel/第一夫人彭丽媛allnorm.xlsx', u'/normExcel/国五条allnorm.xlsx', u'/normExcel/黄浦江死猪allnorm.xlsx',
#      u'/normExcel/撒切尔夫人allnorm.xlsx', u'/normExcel/雅安地震allnorm.xlsx']
    for i in [0]:
        start = datetime.now()
        cope(fold + readfile[i], fold + writefile[i])
        print '处理 %s 花了 %d 秒' % (readfile[i], (datetime.now() - start).seconds)
    
#    cope(u'/tfidfExcel/2013两会1tfidf.xlsx', u'/normExcel/2013两会1norm.xlsx')
        
    print 'done'
