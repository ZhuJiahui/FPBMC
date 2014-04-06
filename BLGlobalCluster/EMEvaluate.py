# -*- coding: utf-8 -*-
'''
Created on 2014年4月2日

@author: ZhuJiahui506
'''
import os
import numpy as np
import time
from TextToolkit import get_text_to_single_list, quick_write_list_to_text

def kmeans_evaluate(read_filename1, read_filename2, write_directory):
    
    # string类型
    real_tag = []
    get_text_to_single_list(real_tag, read_filename1)
    
    cluster_tag = []
    get_text_to_single_list(cluster_tag, read_filename2)
    
    real_tag = real_tag[0 : len(cluster_tag)]
    
    #列表索引+1为聚类编号，等号右边为真实标注的编号 即1对应5...
    reflect_tag = [['6', '8'], ['4'], ['5'], ['7'], ['3'], ['2'], ['6', '8'], ['1']]
    
    cluster_partion = []
    for i in range(len(reflect_tag)):
        cluster_partion.append([])
    
    for i in range(len(cluster_tag)):
        cluster_partion[int(cluster_tag[i]) - 1].append(str(i))
    
    precision_list = []
    recall_list = []
    fmeasure_list = []
    for i in range(len(reflect_tag)):
        real_cluster_partion = []
        for j in range(len(real_tag)):
            if real_tag[j] in reflect_tag[i]:
                real_cluster_partion.append(str(j))
        
        correct = len(set(cluster_partion[i]) & set(real_cluster_partion))
        this_precision = np.true_divide(correct, len(set(cluster_partion[i])))
        this_recall = np.true_divide(correct, len(set(real_cluster_partion)))
        this_fmeasure = np.true_divide(2.0 * this_precision * this_recall, (this_precision + this_recall))
        
        print this_precision, this_recall, this_fmeasure
        
        precision_list.append(str(this_precision))
        recall_list.append(str(this_recall))
        fmeasure_list.append(str(this_fmeasure))
    
    average_precision = np.average([float(x) for x in precision_list])
    average_recall = np.average([float(x) for x in recall_list])
    average_fmeasure = np.average([float(x) for x in fmeasure_list])
    print 'Average:', average_precision, average_recall, average_fmeasure
    quick_write_list_to_text(precision_list, write_directory + u'/precision.txt')
    quick_write_list_to_text(recall_list, write_directory + u'/recall.txt')
    quick_write_list_to_text(fmeasure_list, write_directory + u'/fmeasure.txt')
    
if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/global/weibo_class_tag.txt'
    read_filename2 = root_directory + u'dataset/global_em/cluster_tag2.txt'
    
    write_directory = root_directory + u'dataset/global_em'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)

    kmeans_evaluate(read_filename1, read_filename2, write_directory)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    