# -*- coding: utf-8 -*-
'''
Created on 2014年4月2日

@author: ZhuJiahui506
'''
import os
import numpy as np
import time
from TextToolkit import get_text_to_single_list, quick_write_list_to_text,\
    get_text_to_complex_list


'''
Baseline3  Step 6
Evaluate. EM Cluster

'''

def em_evaluate(read_filename1, read_filename2, write_directory):
    
    # string类型二维列表
    classification_result = []
    get_text_to_complex_list(classification_result, read_filename1, 0)
    
    # string类型
    real_tag = []
    get_text_to_single_list(real_tag, read_filename2)
    
    #列表索引+1为聚类编号，等号右边为真实标注的编号 即1对应5...
    reflect_tag = [['7'], ['1'], ['5'], ['4'], ['3', '2'], ['1'], ['1'], ['1', '2']]
    
    precision_list = []
    recall_list = []
    fmeasure_list = []
    for i in range(len(reflect_tag)):
        real_cluster_partion = []
        for j in range(len(real_tag)):
            if real_tag[j] in reflect_tag[i]:
                real_cluster_partion.append(str(j))
        
        correct = len(set(classification_result[i]) & set(real_cluster_partion))
        this_precision = np.true_divide(correct, len(set(classification_result[i])))
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

    read_filename1 = root_directory + u'dataset/sample_em/classification_result.txt'
    read_filename2 = root_directory + u'dataset/global/weibo_class_tag.txt'
    
    write_directory = root_directory + u'dataset/sample_em'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)

    em_evaluate(read_filename1, read_filename2, write_directory)
       
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    