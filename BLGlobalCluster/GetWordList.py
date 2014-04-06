# -*- coding: utf-8 -*-
'''
Created on 2014年3月27日

@author: ZhuJiahui506
'''

import os
import time
from TextToolkit import quick_write_list_to_text

def get_word_list(read_directory, write_directory):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    for i in range(file_number):
        word_list = []
        
        f = open(read_directory + '/' + str(i + 1) + '.txt', 'r')
        line = f.readline()
        while line:
            for each in line.split():
                if each not in word_list:
                    word_list.append(each)
            line = f.readline()
        f.close()
        
        quick_write_list_to_text(word_list, write_directory + '/' + str(i + 1) + '.txt')

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/segment/weibo_segment'
    write_directory = root_directory + u'dataset/segment/word_list'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    get_word_list(read_directory, write_directory)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    