# -*- coding: utf-8 -*-
'''
Created on 2014年4月3日

@author: ZhuJiahui506
'''
import os
import time
from TextToolkit import quick_write_list_to_text, get_text_to_complex_list


'''
Baseline2 and Baseline3   Step 1
Generate the vector sapce model for K-Means and EM Clustering of the high quality data(8000 Weibo).
Baseline2: K-Means
Baseline3: EM Cluster
'''


'''
Baseline2 and Baseline3   Step 2
K-Means and EM Clustering of the high quality data(8000 Weibo).
We get it in MATLAB. See MATLABMCBaseline/samplekmeans.m  MATLABMCBaseline/sampleem.m
Baseline2: K-Means
Baseline3: EM Cluster
'''


def sample_vsm(read_filename1, read_filename2, write_filename):
    
    weibo_content = []
    all_word_list = []
    
    select_number = 1000
    
    get_text_to_complex_list(weibo_content, read_filename1, 0)
    
    f = open(read_filename2)
    line = f.readline()
    while line:
        all_word_list.append(line.strip().split()[0])
        line = f.readline()  
    f.close()
    
    all_word_list = all_word_list[0 : select_number]
    
    vsm = []
        
    for row in range(len(weibo_content)):
            
        tf_dict = {}  # 词频TF字典
        for key in all_word_list:
            tf_dict[key] = 0
            
        for j in range(len(weibo_content[row])):
            try:
                tf_dict[weibo_content[row][j].split('/')[0]] += 1
            except KeyError:
                tf_dict[weibo_content[row][j].split('/')[0]] = 0
            
        this_line = []
        for key in all_word_list:
            this_line.append(str(tf_dict[key]))
            
        #每一行合并为字符串，方便写入
        vsm.append(" ".join(this_line))
        
    quick_write_list_to_text(vsm, write_filename)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/high_quality_data/weibo_content2.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    
    write_directory = root_directory + u'dataset/high_quality_data'
    write_filename = write_directory + u'/sample_vsm.txt'
    
    sample_vsm(read_filename1, read_filename2, write_filename)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    