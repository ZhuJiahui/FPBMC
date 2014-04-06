# -*- coding: utf-8 -*-
'''
Created on 2014年3月22日

@author: ZhuJiahui506
'''
import os
import time
from TimeConvert import time_convert
from ExcelToolkit import open_sheet
from TextToolkit import quick_write_list_to_text
from operator import itemgetter
from WordSegment import word_segment, get_stopwords1, get_stopwords2

'''
Step 4
Select 8000 Weibo by its EM weights, as well as word segmentation.
'''


def microblog_extract(read_filename, write_directory):
    '''
    选出前8000条微博作为高质量文本并分词，获取微博的各项信息
    :param read_filename:
    :param write_directory:
    '''
    
    #file_number = sum([len(files) for root, dirs, files in os.walk(read_directory)])
    
    select_number = 8000

    stopwords_list1 = get_stopwords1()
    stopwords_list2 = get_stopwords2()
    
    #for i in range(file_number):
        
    high_quality_weibo = []
    high_quality_weibo2 = []
    high_quality_id = []
    high_quality_time = []
    high_quality_tag = []
    
    all_weibo_word = []
        
    weibo_sheet = open_sheet(read_filename)
    weibo_row = weibo_sheet.nrows
    print 'Number of the Weibo row: %d' % weibo_row

    count = 0
    for j in range(1, weibo_row):
            
        weibo_content = str(weibo_sheet.cell(j, 6).value)
        fenci_result = word_segment(weibo_content, stopwords_list1, stopwords_list2)
        if len(fenci_result) > 5 and (" ".join(fenci_result) not in high_quality_weibo):
            count = count + 1
                
            weibo_id = str(int(weibo_sheet.cell(j, 0).value))
            weibo_time = weibo_sheet.cell(j, 2).value
            weibo_time = time_convert(weibo_time)
            
            weibo_tag = str(int(weibo_sheet.cell(j, 5).value))
                
            high_quality_id.append(weibo_id)
            high_quality_time.append(weibo_time)
            high_quality_weibo.append(" ".join(fenci_result))
            fenci_without_tag = [x.split('/')[0] for x in fenci_result]
            high_quality_weibo2.append(" ".join(fenci_without_tag))
            high_quality_tag.append(weibo_tag)
      
            for word in set(fenci_result).difference(all_weibo_word):
                if word not in all_weibo_word:
                    all_weibo_word.append(word)
                        
            if count >= select_number:
                break
    print len(high_quality_weibo)
    
    # 按时间排序
    itw = zip(high_quality_id, high_quality_time, high_quality_weibo, high_quality_weibo2, high_quality_tag)
    itw1 = sorted(itw, key = itemgetter(1))
    
    high_quality_weibo = []
    high_quality_weibo2 = []
    high_quality_id = []
    high_quality_time = []
    high_quality_tag = []
    
    for each in itw1:
        high_quality_id.append(each[0])
        high_quality_time.append(str(each[1]))
        high_quality_weibo.append(each[2])
        high_quality_weibo2.append(each[3])
        high_quality_tag.append(each[4])

    quick_write_list_to_text(high_quality_id, write_directory + '/weibo_id.txt')  
    quick_write_list_to_text(high_quality_time, write_directory + '/weibo_time.txt')
    quick_write_list_to_text(high_quality_weibo, write_directory + '/weibo_content.txt')
    quick_write_list_to_text(high_quality_weibo2, write_directory + '/weibo_content2.txt')
    quick_write_list_to_text(high_quality_tag, write_directory + '/weibo_class_tag.txt')
    quick_write_list_to_text(all_weibo_word, write_directory + '/weibo_word.txt')

    
if __name__=='__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/mixture_data/all.xlsx'
    write_directory = root_directory + u'dataset/high_quality_data'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        
    microblog_extract(read_filename, write_directory)

    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    