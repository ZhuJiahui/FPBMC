# -*- coding: utf-8 -*-
'''
Created on 2014年3月31日

@author: ZhuJiahui506
'''
import os
import numpy as np
import time
from nltk import cluster
from TextToolkit import quick_write_list_to_text, write_matrix_to_text

def batch_em_cluster(read_directory, write_directory1, write_directory2):
    
    file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    cluster_number = 8
    init_mu = 0.1
    init_sigma = 1.0
    
    for i in range(file_number):
        vsm = np.loadtxt(read_directory + '/' + str(i + 1) + '.txt')
        data_dimension = vsm.shape[1]
        
        init_means = []
        for j in range(cluster_number):
            init_means.append(init_sigma * np.random.randn(data_dimension) + init_mu)
        
        cluster_model = cluster.EMClusterer(init_means, bias=0.1)
        
        cluster_tag = cluster_model.cluster(vsm, True, trace=False)
        
        cluster_tag_to_string = [str(x) for x in cluster_tag]
        center_data = cluster_model._means
        
        quick_write_list_to_text(cluster_tag_to_string, write_directory1 + '/' + str(i + 1) + '.txt')
        write_matrix_to_text(center_data, write_directory2 + '/' + str(i + 1) + '.txt')

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_directory = root_directory + u'dataset/segment/vsm2'
    write_directory = root_directory + u'dataset/global_em'
    write_directory1 = write_directory + u'/cluster_tag1'
    write_directory2 = write_directory + u'/cluster_center1'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        os.mkdir(write_directory1)
        os.mkdir(write_directory2)
    if (not(os.path.exists(write_directory1))):
        os.mkdir(write_directory1)
    if (not(os.path.exists(write_directory2))):
        os.mkdir(write_directory2)
    
    batch_em_cluster(read_directory, write_directory1, write_directory2)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    