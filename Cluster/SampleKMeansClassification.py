# -*- coding: utf-8 -*-
'''
Created on 2014年3月28日

@author: ZhuJiahui506
'''
import os
import time
from TextQuery import query2
from TextToolkit import quick_write_list_to_text, get_text_to_complex_list

'''
Baseline2   Step 5
Query. K-Means

'''

def text_classify(read_filename1, read_filename2, read_filename3, write_filename):
    
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
    for i in range(len(search_texts)):
        result.append([])
        
    for i in range(len(query_pattern)):
        this_result = query2(query_pattern[i], search_texts, word_weight_dict)
        result[this_result].append(str(i))
    
    result_to_string = []
    for each in result:
        result_to_string.append(" ".join(each))
    
    quick_write_list_to_text(result_to_string, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/global/weibo_content2.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    read_filename3 = root_directory + u'dataset/sample_kmeans/query_center.txt'
    
    write_directory = root_directory + u'dataset/sample_kmeans'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/classification_result.txt'

    text_classify(read_filename1, read_filename2, read_filename3, write_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'