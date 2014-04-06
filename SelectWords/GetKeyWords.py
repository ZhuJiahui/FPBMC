# -*- coding: utf-8 -*-
'''
Created on 2013年11月14日
Last on 2014年3月23日
@author: ZhuJiahui506
'''

import os
from TextToolkit import get_text_to_complex_list, quick_write_list_to_text
import jieba.analyse
import time

'''
Step 7
Get the key words of the high quality data. Using Jieba analysis.
'''

def get_key_words(read_filename, write_filename1, write_filename2):
    '''
    使用结巴分词获取关键词
    :param read_filename:
    :param write_filename1:
    :param write_filename2:
    '''
    
    each_weibo_fenci = []        
    get_text_to_complex_list(each_weibo_fenci, read_filename, 0)
        
    key_words = []
    all_key_words =  []
    for row in range(len(each_weibo_fenci)):
        word_entity = []

        for each in each_weibo_fenci[row]:
            word_entity.append(each.split('/')[0])

        tags = jieba.analyse.extract_tags(" ".join(word_entity), 3)
        key_words.append(" ".join(tags))
            
        for word in " ".join(tags).split():
            if word not in all_key_words:
                all_key_words.append(word)
        
    quick_write_list_to_text(key_words, write_filename1)
    quick_write_list_to_text(all_key_words, write_filename2)

if __name__ == '__main__':
    start = time.clock()
    now_directory = os.getcwd()
    root_directory = os.path.dirname(now_directory) + '/'
    
    read_filename = root_directory + u'dataset/high_quality_data/weibo_content.txt'
    
    write_directory = root_directory + u'dataset/select_words'
    
    if (not(os.path.exists(write_directory))):
        os.mkdir(write_directory)
    
    write_filename1 = write_directory + u'/key_words.txt'
    write_filename2 = write_directory + u'/all_key_words.txt'
    
    get_key_words(read_filename, write_filename1, write_filename2)
    
    print 'Total time %f seconds' % (time.clock() - start)
    print 'Complete !!!'