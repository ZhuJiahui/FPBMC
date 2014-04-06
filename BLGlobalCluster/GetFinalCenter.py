# -*- coding: utf-8 -*-
'''
Created on 2014年3月29日

@author: ZhuJiahui506
'''

import os
import numpy as np
from Reflect import reflect_vsm_to_wordlist
from TextToolkit import quick_write_list_to_text, get_text_to_single_list
import time

def get_final_center(read_filename1, read_filename2, write_filename):

    result = []

        
    word_list = []
    get_text_to_single_list(word_list, read_filename2)
        
    vsm = np.loadtxt(read_filename1)
    vsm = vsm.T
    for each in vsm:
        result.append(" ".join(reflect_vsm_to_wordlist(each, word_list)))
    
    quick_write_list_to_text(result, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/global_em/cluster_center2.txt'
    read_filename2 = root_directory + u'dataset/global_em/new_word_list.txt'
    #read_filename1 = root_directory + u'dataset/global_kmeans/cluster_center2.txt'
    #read_filename2 = root_directory + u'dataset/global_kmeans/new_word_list.txt'

    write_filename = root_directory + u'dataset/global_em/real_cluster_center.txt'
    #write_filename = root_directory + u'dataset/global_kmeans/real_cluster_center.txt'
    
    get_final_center(read_filename1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    