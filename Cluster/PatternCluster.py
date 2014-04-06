# -*- coding: utf-8 -*-
'''
Created on 2014年3月27日

@author: ZhuJiahui506
'''
import os
import time
from Cluster.ComputeSimilarity import compute_similarity
from TextToolkit import write_matrix_to_text, quick_write_list_to_text


'''
Step 10
Compute the Similarity Matrix of the frequent patterns for Spectral Clustering, 
and generate the cluster number at the same time.

See also ComputeSimilarity.py and TextQuery.py
'''

'''
Step 11
Spectral Clustering
As Python is not good at computing the eigen values and eigen vectors of the large matrix
So we cope the #Step 11# in MATLAB
'''

def pattern_cluster(read_filename1, read_filename2, read_filename3, write_filename1, write_filename2):
    pattern_list = []
    f = open(read_filename1, 'r')
    line = f.readline()
    while line:
        if len(line.split()) > 1:
            pattern_list.append(line.split())
        line = f.readline()
    f.close()
    
    word_weight_dict = {}
    f = open(read_filename2, 'r')
    line = f.readline()
    while line:
        word_weight_dict[line.split()[0]] = float(line.split()[1])
        line = f.readline()
    f.close()
    
    #调用compute_similarity函数计算相似度矩阵并给出聚类数目
    similarity_matrix, cluster_number = compute_similarity(pattern_list, read_filename3, word_weight_dict)
    
    write_matrix_to_text(similarity_matrix, write_filename1)
    quick_write_list_to_text([str(cluster_number)], write_filename2)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    #####可在上一步的基础上观察不同最小支持度和相似度阈值下聚类数目的变化，作为实验对比
    #read_filename1 = root_directory + u'dataset/frequent_patterns25/real_word_trans.txt'
    #####
    read_filename1 = root_directory + u'dataset/frequent_patterns/real_word_trans.txt'
    read_filename2 = root_directory + u'dataset/select_words/top_n_words.txt'
    read_filename3 = root_directory + u'dataset/high_quality_data/weibo_content2.txt'
    
    write_directory = root_directory + u'dataset/cluster25'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename1 = write_directory + u'/similarity_matrix.txt'
    write_filename2 = write_directory + u'/cluster_number.txt'
    #write_filename3 = write_directory + u'/pre_query_result.txt'

    pattern_cluster(read_filename1, read_filename2, read_filename3, write_filename1, write_filename2)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    