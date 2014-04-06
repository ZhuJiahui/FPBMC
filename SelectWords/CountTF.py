# -*- coding: utf-8 -*-
'''
Created on 2013年11月14日
Last on 2014年3月23日
@author: ZhuJiahui506
'''

import os
from operator import itemgetter
from TextToolkit import get_text_to_single_list, get_text_to_complex_list, quick_write_list_to_text
import time

'''
Step 6
Count the TF for all the words in the high quality Weibo.
'''

def count_word_tf(read_filename1, read_filename2, write_filename):
    '''
    计算数据的所有词汇的词频
    :param read_filename1:
    :param read_filename2:
    :param write_filename:
    '''
    
    each_weibo_fenci = [] 
    all_weibo_fenci = []
        
    get_text_to_complex_list(each_weibo_fenci, read_filename1, 0)
    get_text_to_single_list(all_weibo_fenci, read_filename2)
        
    tf_dict = {}  #词频TF字典
    for key in all_weibo_fenci:
        tf_dict[key] = 0
            
    for row in range(len(each_weibo_fenci)):
        for j in range(len(each_weibo_fenci[row])):
            try:
                tf_dict[each_weibo_fenci[row][j]] += 1
            except KeyError:
                tf_dict[each_weibo_fenci[row][j]] = 0
        
    #词频列表
    value_list = []
    for key in all_weibo_fenci:
        value_list.append(tf_dict[key])
        
    # 按词频降序排序
    va = zip(all_weibo_fenci, value_list)
    va = sorted(va, key = itemgetter(1), reverse = True)    
        
    result_all = []
    for each in va:
        result_all.append(each[0] + " " + str(each[1]))
       
    quick_write_list_to_text(result_all, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    write_directory = root_directory + u'dataset/select_words'
    
    read_filename1 = root_directory + u'dataset/high_quality_data/weibo_content.txt'
    read_filename2 = root_directory + u'dataset/high_quality_data/weibo_word.txt'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/tf_all.txt'
    
    count_word_tf(read_filename1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    