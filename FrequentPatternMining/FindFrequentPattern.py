# -*- coding: utf-8 -*-
'''
Created on 2014年3月23日

@author: ZhuJiahui506
'''
import os
import time
import numpy as np
from operator import itemgetter
from fp_growth import find_frequent_itemsets
from TextToolkit import quick_write_list_to_text

'''
Step 9
Mining the frequent patterns for the high quality data(8000 Weibo). Using FP-Groth
In our paper: minimun_support = 25, similarity : 0.4999
'''

def generate_transactions(read_filename, word_list):
    '''
    将向量空间矩阵转化为事务列表
    :param read_filename: 向量空间文件
    '''
    trans = []
    
    f = open(read_filename, 'rb')
    line = f.readline()
    while line:
        temp_trans = []
        word_with_tag = line.split()

        for each1 in word_with_tag:
            word_entity = each1.split('/')[0]
            if word_entity in word_list:
                word_index = word_list.index(word_entity)
                if word_index not in temp_trans:
                    temp_trans.append(word_index)
        
        trans.append(temp_trans)
        line = f.readline()
    f.close()
    
    #返回事务表示，（每一行是一个事务，事务由项组成）
    #trans是int型的二维列表
    return trans

def map_trans_to_word(tran, word_list):
    '''
    将事务表达式还原为词汇列表
    :param tran:
    :param word_list:
    '''
    real_word_list = []
    for index1 in tran:
        real_word_list.append(word_list[index1])
    
    return real_word_list

def find_frequent_pattern(read_filename1, read_filename2, write_filename1, write_filename2, write_filename3):
    
    #频繁项集挖掘的支持度
    ##### 可调整该值输出不同的结果，作为实验对比
    minimun_support = 25
    #####
    
    #频繁项及其对应的长度、支持度的列表
    frequent_patterns = []  #二维int列表
    length_all = []
    support_all = []
    
    word_list = []
    f0 = open(read_filename2, 'rb')
    line = f0.readline()
    while line:
        word_list.append(line.split()[0])
        line = f0.readline()
    f0.close()
    
    '''
    #挖掘频繁项集，并得到相应的频繁项集的支持度
    #频繁项集挖掘采用FP-Growth算法
    #参考 https://github.com/enaeseth/python-fp-growth
    '''
    trans = generate_transactions(read_filename1, word_list)
    
    #find_frequent_itemsets返回的结果类型为"generator"
    #The type of the return of the "find_frequent_itemsets" is "generator"
    for each, support in find_frequent_itemsets(trans, minimun_support, include_support=True):
        each.sort()
               
        frequent_patterns.append(each)
        length_all.append(len(each))
        support_all.append(support)
        
    print 'Total frequent patterns: %d' % len(frequent_patterns)           
    
    #频繁项按照长度由高到低排序
    fl = zip(frequent_patterns, length_all, support_all)
    fl1 = sorted(fl, key = itemgetter(1), reverse = True)
    
    frequent_patterns = []
    result_length_support = []
    
    #频繁项集过滤
    for each in fl1:
        
        tag = 0
        for each1 in frequent_patterns:
            if len(set(each[0]) & set(each1)) == len(each[0]):
                tag = 1
                break
            elif np.true_divide(len(set(each[0]) & set(each1)), len(set(each[0]) | set(each1))) > 0.4999:
                ##### 可调整该相似度，作为实验对比
                #####
                tag = 1
                break
            else:
                pass
            
        if tag == 0:               
            frequent_patterns.append(each[0])
            result_length_support.append(str(each[1]) + " " + str(each[2]))
    
    #result_length_support = []
    
    real_word_trans = []
    trans_to_string = []
    
    for each in frequent_patterns:
        trans_to_string.append(" ".join([str(x) for x in each]))
        real_word_list = map_trans_to_word(each, word_list)
        real_word_trans.append(" ".join(real_word_list))
    
    quick_write_list_to_text(trans_to_string, write_filename1)
    quick_write_list_to_text(result_length_support, write_filename2)
    quick_write_list_to_text(real_word_trans, write_filename3)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/high_quality_data/weibo_content.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'

    #write_directory = root_directory + u'dataset/frequent_patterns20'
    #write_directory = root_directory + u'dataset/frequent_patterns25'
    #write_directory = root_directory + u'dataset/frequent_patterns30'
    write_directory = root_directory + u'dataset/frequent_patterns'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename1 = write_directory + u'/trans.txt'
    write_filename2 = write_directory + u'/length_support.txt'
    write_filename3 = write_directory + u'/real_word_trans.txt'
    
    find_frequent_pattern(read_filename1, read_filename2, write_filename1, write_filename2, write_filename3)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    