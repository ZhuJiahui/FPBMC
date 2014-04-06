# -*- coding: utf-8 -*-
'''
Created on 2014年3月25日

@author: ZhuJiahui506
'''
import os
import time
from TextToolkit import quick_write_list_to_text, get_text_to_single_list

'''
Step 3
Compute EM weight of each Weibo and ordered by its EM weights.  Using Excel to cope with the sort. 
So the original data was changed. See all.xlsx
'''


def compute_em_weights(read_filename1, read_filename2, write_filename):
    '''
    Linear fusion
    :param read_filename1:
    :param read_filename2:
    :param write_filename:
    '''

    em_weights = []
    
    coefficients_string = [] 
    get_text_to_single_list(coefficients_string, read_filename2)   
    coefficients = [float(x) for x in coefficients_string]
        
    f = open(read_filename1, 'r')
    line = f.readline()
    while line:
        each_line = line.split()
        em_weights.append(float(each_line[0]) * coefficients[0] + float(each_line[1]) * coefficients[1] + float(each_line[2]) * coefficients[2])
            
        line = f.readline()
    f.close()
    
    em_weights_to_string = [str(x) for x in em_weights]
    quick_write_list_to_text(em_weights_to_string, write_filename)
    
if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename1 = root_directory + u'dataset/em/score.txt'
    read_filename2 = root_directory + u'dataset/em/em_coefficients.txt'
    write_filename = root_directory + u'dataset/em/all_em_weights.txt'

    compute_em_weights(read_filename1, read_filename2, write_filename)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    