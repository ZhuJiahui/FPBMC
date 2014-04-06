# -*- coding: utf-8 -*-
'''
Created on 2013年11月22日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text

def data_segment(read_filename, write_directory):
    '''
    数据分片
    :param read_filename: 读取文件
    :param write_directory: 写入目录
    '''
    
    # 文件开始的编号
    file_number = 1
    
    print "Begin data segmentation!!!" 
    print "May take a long time, Please Wait..."
        
    # 每条微博的分词
    weibo_content_segment = []
    
    # 每条文本的分词
    weibo_id_segment = []

    line_count = 0
    
    fr = open(read_filename)
    line = fr.readline()
    while line:
        weibo_content_segment.append(line.strip())
        weibo_id_segment.append(str(line_count))
        line_count += 1
        
        if line_count % 5000 == 0:
            # 写入文件
            quick_write_list_to_text(weibo_content_segment, write_directory + u'/weibo_segment/' + str(file_number) + '.txt')
            quick_write_list_to_text(weibo_id_segment, write_directory + u'/weibo_id/' + str(file_number) + '.txt')
            file_number += 1
            weibo_content_segment = []
            weibo_id_segment = []
            
        line = fr.readline()     
    fr.close()

    print "Data Segmentation Complete!!!"
    print "Total Segments: %d" % (file_number - 1)    

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/global/weibo_content.txt'
    write_directory = root_directory + u'dataset/segment'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory + u'/weibo_segment')
        os.mkdir(write_directory + u'/weibo_id')
        
    if (not(os.path.exists(write_directory + u'/weibo_segment'))):
        os.mkdir(write_directory + u'/weibo_segment')
        
    if (not(os.path.exists(write_directory + u'/weibo_id'))):
        os.mkdir(write_directory + u'/weibo_id')

    
    data_segment(read_filename, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    
    
