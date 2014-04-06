# -*- coding: utf-8 -*-
'''
Created on 2014年3月27日

@author: ZhuJiahui506
'''
import numpy as np

'''
Query for the frequent patterns. 2 modes.
'''

def query(pattern, search_texts, word_weight_dict):
    '''
    用频繁项集查询全局文本，即将频繁项集映射到全局微博文本
    :param pattern:
    :param search_texts:
    :param word_weight_dict:
    '''
    
    #检索阈值
    BETA = 3.0

    query_result = []
    for i in range(len(search_texts)):
        temp_weight = 0.0
        for each in pattern:
            tf = search_texts[i].count(each)
            if tf > 0:
                temp_weight += tf * word_weight_dict[each]
        
        if temp_weight >= BETA:
            query_result.append(i)
    
    return query_result

def query2(pattern, search_texts, word_weight_dict):
    '''
    用微博文本查询频繁项集，即将微博文本映射到频繁项集，文本只属于与之最相似的那个频繁项集所代表的类
    :param pattern:
    :param search_texts:
    :param word_weight_dict:
    '''

    query_result = []
    for i in range(len(search_texts)):
        temp_weight = 0.0
        for each in pattern:
            tf = search_texts[i].count(each)
            if tf > 0 and each in word_weight_dict.keys():
                temp_weight += tf * word_weight_dict[each]
                
        query_result.append(temp_weight)
    
    max_index = np.argmax(query_result)
    
    return max_index

if __name__ == '__main__':
    pass