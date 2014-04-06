# -*- coding: utf-8 -*-
'''
Created on 2014年3月27日

@author: ZhuJiahui506
'''
import os
import time
import numpy as np
from TextToolkit import quick_write_list_to_text

'''
Baseline1 Step 1
Generate the vector sapce of the frequent patterns for K-Means and Spectral Clustering.
'''


'''
Baseline1 Step 2
Using the vector sapce model for K-Means and Spectral Clustering.
We get it in MATLAB.
'''

def generate_vsm_for_trans(read_filename):
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    write_directory = root_directory + u'dataset'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/vsm.txt'
    
    pattern_list = []
    all_word_list = []
    
    f = open(read_filename, 'r')
    line = f.readline()
    while line:
        if len(line.split()) > 1:
            pattern_list.append(line.split())
            for each in line.split():
                if each not in all_word_list:
                    all_word_list.append(each)
        line = f.readline()
    f.close()
    
    vsm = []
    
    for i in range(len(pattern_list)):
        tf_dict = {}  # 词频TF字典
        for key in all_word_list:
            tf_dict[key] = 0
            
        for each in pattern_list[i]:
            try:
                tf_dict[each] = 1
            except KeyError:
                tf_dict[each] = 0
            
        this_line = []
        for key in all_word_list:
            this_line.append(tf_dict[key])
        
        vsm.append(this_line)
    
    vsm_to_string = []
    for each in vsm:
        vsm_to_string.append(" ".join([str(x) for x in each]))
    
    np_vsm = np.array([vsm])
    
    quick_write_list_to_text(vsm_to_string, write_filename)
    return np_vsm

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/frequent_patterns/real_word_trans.txt'
    
    generate_vsm_for_trans(read_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    