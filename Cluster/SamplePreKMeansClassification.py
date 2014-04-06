# -*- coding: utf-8 -*-
'''
Created on 2014年3月28日

@author: ZhuJiahui506
'''
import os
import time
import numpy as np
from operator import itemgetter
from TextToolkit import quick_write_list_to_text

'''
Baseline2   Step 4
Generate the query patterns(After K-Means).

'''

def pre_text_classify(read_filename1, read_filename2, write_filename):
    
    vsm = np.loadtxt(read_filename1)
    vsm = vsm.T
    
    select_number = 3
    
    word_list = []
    word_weight = []
    #word_weight_dict = {}
    f = open(read_filename2, 'r')
    line = f.readline()
    while line:
        word_list.append(line.split()[0])
        word_weight.append(line.split()[1])

        line = f.readline()
    f.close()
    
    word_list = word_list[0:1000]
    word_weight = word_weight[0:1000]
    
    total_result = []
    for i in range(len(vsm)):
        weight = []
        for j in range(len(word_list)):
            weight.append(vsm[i, j])
        
        ww = zip(word_list, weight)
        ww = sorted(ww, key = itemgetter(1), reverse = True)
        
        word_result = []
        count_number = 1
        for each in ww:
            word_result.append(each[0])
            count_number += 1
            if count_number > select_number:
                break
        total_result.append(" ".join(word_result))
    
    quick_write_list_to_text(total_result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/sample_kmeans/cluster_center.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    
    write_directory = root_directory + u'dataset/sample_kmeans'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/query_center.txt'

    pre_text_classify(read_filename1, read_filename2, write_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'