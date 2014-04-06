# -*- coding: utf-8 -*-
'''
Created on 2014年3月29日

@author: ZhuJiahui506
'''

import os
import numpy as np
from Reflect import reflect_vsm_to_wordlist
from TextToolkit import quick_write_list_to_text
import time

'''
Baseline2 and Baseline3   Step 3
The center word list of K-Means and EM Clustering of the high quality data(8000 Weibo).

Baseline2: K-Means
Baseline3: EM Cluster
'''


def sample_real_center(read_filename1, read_filename2, write_filename):

    result = []
  
    word_list = []
    f = open(read_filename2)
    line = f.readline()
    while line:
        word_list.append(line.strip().split()[0])
        line = f.readline()  
    f.close()
    
    word_list = word_list[0 : 1000]
        
    vsm = np.loadtxt(read_filename1)
    vsm = vsm.T
    for each in vsm:
        result.append(" ".join(reflect_vsm_to_wordlist(each, word_list)))
    
    quick_write_list_to_text(result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/sample_em/cluster_center.txt'
    #read_filename1 = root_directory + u'dataset/sample_sc/cluster_center.txt'
    #read_filename1 = root_directory + u'dataset/sample_kmeans/cluster_center.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    
    write_directory = root_directory + u'dataset/sample_em'
    #write_directory = root_directory + u'dataset/sample_sc'
    #write_directory = root_directory + u'dataset/sample_kmeans'
    write_filename = write_directory + u'/real_cluster_center.txt'

    
    sample_real_center(read_filename1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    