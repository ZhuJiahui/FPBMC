# -*- coding: utf-8 -*-
'''
Created on 2014年3月28日

@author: ZhuJiahui506
'''
import os
import time
from TextQuery import query
from TextToolkit import quick_write_list_to_text, get_text_to_complex_list

'''
Step 13
Query: given the cluster center word list,search in the gloabal Weibo text. 
'''

def text_classify(read_filename1, read_filename2, read_filename3, write_filename):
    '''
    查询分类
    :param read_filename1:
    :param read_filename2:
    :param read_filename3:
    :param write_filename:
    '''
    
    query_pattern = []
    get_text_to_complex_list(query_pattern, read_filename1, 0)
    
    word_weight_dict = {}
    f = open(read_filename2, 'r')
    line = f.readline()
    while line:
        word_weight_dict[line.split()[0]] = float(line.split()[1])
        line = f.readline()
    f.close()
    
    search_texts = []
    f1 = open(read_filename3, 'r')
    line = f1.readline()
    while line:
        search_texts.append(line.strip())
        line = f1.readline()  
    f1.close()
    
    result = []
    for i in range(len(query_pattern)):
        this_result = query(query_pattern[i], search_texts, word_weight_dict)
        result.append(" ".join([str(x) for x in this_result]))
    
    quick_write_list_to_text(result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/cluster7/cluster_word_list.txt'
    #read_filename1 = root_directory + u'dataset/cluster/cluster_word_list.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    read_filename3 = root_directory + u'dataset/global/weibo_content2.txt'
    
    write_directory = root_directory + u'dataset/cluster7'
    #write_directory = root_directory + u'dataset/cluster'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/classification_result.txt'

    text_classify(read_filename1, read_filename2, read_filename3, write_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'