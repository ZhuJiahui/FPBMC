# -*- coding: utf-8 -*-
'''
Created on 2014年3月24日

@author: ZhuJiahui506
'''
import os
import time
import re
import numpy as np
from ExcelToolkit import open_sheet
from TextToolkit import quick_write_list_to_text

'''
Warning The original Excel data was not oerderd by EM weight. See all_pre.xlsx
Step 1
'''

def score_normalize(data_list, per, enlar):

    max_data = np.max(data_list)
    min_data = np.min(data_list)
    percent = (max_data - min_data) * per
    
    result = []

    for i in range(len(data_list)):
        result.append((data_list[i] - min_data + percent) / (max_data - min_data + percent) * enlar)
    
    return result

def log_score_normalize(data_list, per, enlar):

    log_data = []
    for each in data_list:
        if each <= 0:
            log_data.append(0.0)
        else:
            log_data.append(np.log(each + 1.0))
    
    result = score_normalize(log_data, per, enlar)
    
    return result

def t_log_score_normalize(data_list, per, enlar):
    '''
    log10 normalize
    :param data_list:
    :param per:
    :param enlar:
    '''

    log_data = []
    for each in data_list:
        if each <= 0:
            log_data.append(0.0)
        else:
            log_data.append(np.log10(each + 1.0))
    
    result = score_normalize(log_data, per, enlar)
    
    return result

def feature_scoring(read_directory, write_directory):
     
    pa = 'http://[\w\.\*\?-_#/]*(?=\b)?'
    per = 0.05
    enlar = 100.0
        
    weibo_sheet = open_sheet(read_filename)
    weibo_row = weibo_sheet.nrows
    print 'Number of the Weibo row: %d' % weibo_row
        
    forwards = []
    comments = []
    urls = []
        
    url_dict = {}

    for j in range(1, weibo_row):      
                
        forwards.append(int(weibo_sheet.cell(j, 3).value))
        comments.append(int(weibo_sheet.cell(j, 4).value))

        weibo_content = str(weibo_sheet.cell(j, 6).value)
        try:             
            matches = re.findall(pa, weibo_content)
            for ma in matches:
                if ma in url_dict:
                    url_dict[ma] += 1
                else:
                    url_dict[ma] = 1
            urls.append(matches)
        except Exception, e:
            print e
            print (j + 1)
            urls.append([])
        
    url_score = []
    for j in range(len(forwards)):
        if len(urls[j]) > 0:
            sum_score = 0
            for each in urls[j]:
                sum_score += url_dict[each]
            url_score.append(sum_score)
        else:
            url_score.append(0)
    
    forwards_norm = log_score_normalize(forwards, per, enlar)
    comments_norm = log_score_normalize(forwards, per, enlar)
    urls_norm = t_log_score_normalize(url_score, per, enlar)
        
    result_all = []
    for j in range(len(forwards)):
        result_all.append(str(forwards_norm[j]) + " " + str(comments_norm[j]) + " " + str(urls_norm[j]))
   
    quick_write_list_to_text(result_all, write_filename)

  
if __name__=='__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/mixture_data/all.xlsx'
    write_directory = root_directory + u'dataset/em'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename = write_directory + u'/score.txt'
    feature_scoring(read_filename, write_filename)

    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    