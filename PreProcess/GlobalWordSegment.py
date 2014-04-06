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
from WordSegment import word_segment, get_stopwords1, get_stopwords2

'''
Step 5
Word segmentation for all the Weibo. For comparation.
'''

def global_segment(read_filename, write_directory):
    '''
    所有微博文本分词，并获取微博的各项信息
    :param read_filename:
    :param write_directory:
    '''

    stopwords_list1 = get_stopwords1()
    stopwords_list2 = get_stopwords2()
        
    global_id = []
    global_time = []
    global_tag = []

    weibo_sheet = open_sheet(read_filename)
    weibo_row = weibo_sheet.nrows
    print 'Number of the Weibo row: %d' % weibo_row
    
    f1 = open(write_directory + '/weibo_content.txt', 'w')
    f2 = open(write_directory + '/weibo_content2.txt', 'w')

    for j in range(1, weibo_row):
       
        weibo_id = str(int(weibo_sheet.cell(j, 0).value))
        weibo_time = weibo_sheet.cell(j, 2).value
        weibo_time = time_convert(weibo_time)
            
        weibo_tag = str(int(weibo_sheet.cell(j, 5).value))
                
        global_id.append(weibo_id)
        global_time.append(str(weibo_time))
        
        weibo_content = str(weibo_sheet.cell(j, 6).value)
        fenci_result = word_segment(weibo_content, stopwords_list1, stopwords_list2)
        f1.write(" ".join(fenci_result))
        f1.write("\n")
        
        fenci_without_tag = [x.split('/')[0] for x in fenci_result]
        f2.write(" ".join(fenci_without_tag))
        f2.write("\n")
        global_tag.append(weibo_tag)
    
    f1.close()
    f2.close()

    quick_write_list_to_text(global_id, write_directory + '/weibo_id.txt')  
    quick_write_list_to_text(global_time, write_directory + '/weibo_time.txt')
    quick_write_list_to_text(global_tag, write_directory + '/weibo_class_tag.txt')
  
if __name__=='__main__':
    
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/mixture_data/all.xlsx'
    write_directory = root_directory + u'dataset/global'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
        
    global_segment(read_filename, write_directory)

    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'
    