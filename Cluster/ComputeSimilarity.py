# -*- coding: utf-8 -*-
'''
Created on 2014年3月26日

@author: ZhuJiahui506
'''
import os
import time
import numpy as np
from operator import itemgetter
from TextQuery import query
from TextToolkit import get_text_to_single_list, quick_write_list_to_text

'''
Function for compute similarity matrix and cluster number.

'''

def compute_similarity(pattern_list, read_filename, word_weight_dict):

    search_texts = []
    get_text_to_single_list(search_texts, read_filename)
    
    query_result_list = []
    for i in range(len(pattern_list)):
        query_result_list.append(query(pattern_list[i], search_texts, word_weight_dict))
    
    similarity_matrix = np.zeros([len(pattern_list), len(pattern_list)])
    tag = []
    for i in range(len(pattern_list)):
        tag.append(0)
        for j in range(i, len(pattern_list)):
            '''
            计算每一个频繁项集查询匹配到的文本集合，用查询文本集合之间的Jacard相似度衡量频繁项集之间的相似度
            见TextQuery.py
            '''
            numerator = len(set(query_result_list[i]) & set(query_result_list[j]))
            denominator = len(set(query_result_list[i]) | set(query_result_list[j]))
            
            similarity_matrix[i, j] = np.true_divide(numerator, denominator)
            similarity_matrix[j, i] = similarity_matrix[i, j]
    
    '''
    分部划分以确定聚类中心个数
    '''       
    class_partion = []        
    for i in range(len(pattern_list)):
        if tag[i] == 0:
            temp_class_partion = []
            for j in range(i, len(pattern_list)):
                if similarity_matrix[i, j] > 0.2:
                    temp_class_partion.append(j)
                    tag[j] = 1
            class_partion.append(temp_class_partion)
    
    partion_length = []
    for each in class_partion:
        partion_length.append(len(each))
    
    # 按长度降序排序
    cl = zip(class_partion, partion_length)
    cl = sorted(cl, key = itemgetter(1), reverse = True)
    
    class_partion = []
    partion_length = []
    
    for each in cl:
        class_partion.append(each[0])
        partion_length.append(each[1])
    
    length_sum = np.sum(partion_length)
    temp_sum = 0
    cluster_number = 0
    for i in range(len(partion_length)):
        temp_sum += partion_length[i]
        cluster_number += 1
        
        #选取所有频繁项集数量的75%，一刀切，前面的部分的划分数就是聚类数目
        if np.true_divide(temp_sum, length_sum) > 0.75:
            break

    class_partion_to_string = []
    for i in range(cluster_number):
        class_partion_to_string.append(" ".join([str(x) for x in class_partion[i]]))
        
    print cluster_number
    
    query_result_list_string = []
    for each in query_result_list:
        query_result_list_string.append(" ".join([str(x) for x in each]))       
    
    # if possible  
    #quick_write_list_to_text(class_partion_to_string, 'D:/partion2.txt')
    
    return similarity_matrix, cluster_number
        

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
#     read_filename1 = root_directory + u'dataset/frequent_patterns/real_word_trans.txt'
#     read_filename2 = root_directory + u'dataset/high_quality_data/weibo_content2.txt'
#     read_filename3 = root_directory + u'dataset/select_words/top_n_words.txt'
# 
#     write_directory = root_directory + u'dataset/cluster'
#     
#     if (not(os.path.exists(write_directory))):
#         os.mkdir(write_directory)
#     
    #write_filename1 = write_directory + u'/pre_similarity_matrix.txt'
    #write_filename2 = write_directory + u'/pre_class_partion.txt'
    #write_filename3 = write_directory + u'/pre_query_result.txt'

    #compute_similarity(read_filename1, read_filename2, read_filename3)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    