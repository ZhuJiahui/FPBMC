# -*- coding: utf-8 -*-
'''
Created on 2014年3月29日

@author: ZhuJiahui506
'''
import os
import time
from operator import itemgetter
import numpy as np
from TextToolkit import get_text_to_single_list, get_text_to_complex_list,\
    quick_write_list_to_text

'''
Step 12
Generate the cluster word list for query.
It is reconmented that the query length is no longer than 3
Finally in our paper, we set the cluster number=7, not 8(generate in the experiment)
'''

def pre_text_classify(read_filename1, read_filename2, read_filename3, write_filename):
    
    #展示5个词汇
    #查询时选取3个词汇
    select_number = 5
    
    # 频繁项集聚类的结果标号,string类型，从1开始
    class_tag = []
    get_text_to_single_list(class_tag, read_filename1)

    # 聚簇数目
    cluster_number = len(set(class_tag))
    
    # 频繁项集，二维string类型列表
    pattern_all = []
    get_text_to_complex_list(pattern_all, read_filename2, 0)
    pattern_all = pattern_all[0: len(class_tag)]
    
    # 获得聚类结果的频繁项集划分，int型二维列表
    class_partion = []
    for i in range(cluster_number):
        class_partion.append([])
        
    for i in range(len(class_tag)):
        for j in range(cluster_number):
            if class_tag[i] == str(j + 1):
                class_partion[j].append(i)
    
    # 获取全局词汇的权值
    word_weight_dict = {}
    f = open(read_filename3, 'r')
    line = f.readline()
    while line:
        word_weight_dict[line.split()[0]] = float(line.split()[1])
        line = f.readline()
    f.close()
    
    # 获取频繁项集中所有不同的词汇
    all_word_list = []
    for each in pattern_all:
        for word in set(each).difference(all_word_list):
            all_word_list.append(word)
    
    # 包含某个单词的频繁项集个数——针对所有单词
    I_dict = {}
    for each in all_word_list:
        I_dict[each] = 0
        for each1 in pattern_all:
            if each in each1:
                I_dict[each] += 1
    
    # 包含某个单词的聚簇个数——针对所有单词
    C_dict = {}
    for each in all_word_list:
        C_dict[each] = 0
        for i in range(len(class_partion)):
            for j in range(len(class_partion[i])):
                if each in pattern_all[class_partion[i][j]]:
                    C_dict[each] += 1
                    break
    
    cluster_word_list = []   
    for i in range(len(class_partion)):
        # 获取该聚簇下所有不同的单词
        this_word_list = []
        for j in range(len(class_partion[i])):
            for each in pattern_all[class_partion[i][j]]:
                if each not in this_word_list:
                    this_word_list.append(each)
        
        # 计算每个单词在聚簇中的支持度
        sup_dict = {}
        
        for each in this_word_list:
            sup_dict[each] = 0
            for j in range(len(class_partion[i])):
                if each in pattern_all[class_partion[i][j]]:
                    sup_dict[each] += 1
        
        word_score_list = []
        # 计算聚簇中的每个单词的权值，作为查询分类的依据
        for each in this_word_list:
            global_weight = np.true_divide(len(pattern_all) * cluster_number, (I_dict[each] * C_dict[each])) 
            word_score = word_weight_dict[each] * sup_dict[each] * np.log(global_weight + 1.0)
            word_score_list.append(word_score)
        
        # 按权值降序排序
        tw = zip(this_word_list, word_score_list)
        tw = sorted(tw, key = itemgetter(1), reverse = True)
        
        this_word_list = []
        word_score_list = []
        
        count = 0
        for each in tw:
            this_word_list.append(each[0])
            count += 1
            if count >= select_number:
                break
        
        cluster_word_list.append(" ".join(this_word_list))
    
    quick_write_list_to_text(cluster_word_list, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #read_filename1 = root_directory + u'dataset/cluster/sc-result-labels.txt'
    ##### 聚不同个数的类 7或9，作为实验对比
    #read_filename1 = root_directory + u'dataset/cluster9/sc-result-labels.txt'
    read_filename1 = root_directory + u'dataset/cluster7/sc-result-labels.txt'
    #####
    read_filename2 = root_directory + u'dataset/frequent_patterns/real_word_trans.txt'
    read_filename3 = root_directory + u'dataset/select_words/top_n_words.txt'
    
    #write_directory = root_directory + u'dataset/cluster'
    #write_directory = root_directory + u'dataset/cluster9'
    write_directory = root_directory + u'dataset/cluster7'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/cluster_word_list.txt'

    pre_text_classify(read_filename1, read_filename2, read_filename3, write_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    