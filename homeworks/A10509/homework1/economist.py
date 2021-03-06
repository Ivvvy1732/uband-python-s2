# -*- coding: utf-8 -*-

import codecs
import os
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def read_file(file_path):
    f = codecs.open(file_path, 'r') #打开文件
    lines = f.readlines()
    word_list = []
    for line in lines:
        line = line.strip()
        words = line.split(" ") #用空格分割
        words = word_split(words) #用-分割
        word_list.extend(words)
    return word_list

def get_file_from_folder(folder_path):
    file_paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths


#读取多文件里的单词
def read_files(file_paths):
    final_words = []
    for path in file_paths:
        final_words.extend(read_file(path))
    return final_words

def word_split(words):
    new_list = []
    for word in words:
        if '-' not in word:
            new_list.append(word)
        else:
            lst = word.split('-')
            new_list.extend(lst)
    return new_list

#2.获取格式化之后的单词
def format_word(word):
    fmt = 'abcdefghijklmnopqrstuvwxyz-'
    for char in word:
        if char not in fmt:
            word = word.replace(char, '')
    return word.lower()

def format_words(words):
    word_list = []
    for word in words:
        wd = format_word(word)
        if wd:
            word_list.append(wd)
    return word_list

#统计单词数目好和排序
def statictcs_words(words):
    s_word_dict = {}
    for word in words:
        if s_word_dict.has_key(word):
            s_word_dict[word] = s_word_dict[word] + 1
        else:
            s_word_dict[word] = 1
    #排序
    sorted_dict = sorted(s_word_dict.iteritems(), key=lambda d: d[1], reverse=True)
    return sorted_dict


#读取词典文件
def read_dict(file_path):
    f = codecs.open(file_path, 'r', "utf-8") 
    lines = f.readlines()
    word_dict = {}
    for line in lines:
        line = line.strip()
        word, space, meaning = line.partition(' ') #以空格区分单词与释义
        meaning = meaning.strip()
        if word:
            word_dict[word] = meaning
    return word_dict



#输出成csv
def print_to_csv(volcaulay_list, word_dict, to_file_path, total_count, start_and_end):
    nfile = codecs.open(to_file_path, 'w+', "utf-8")
    current_count = 0
    for val in volcaulay_list:
        num = val[1]
        current_count = current_count + num
        word_rate = (float(current_count)/total_count) * 100
        meaning = u'未找到释义'
        if val[0] in word_dict:
            meaning = word_dict[val[0]]
        if (word_rate/100 >= start_and_end[0]) and (word_rate/100 <=start_and_end[1]):
            nfile.write("%s,%d,%0.2f,%s\n" % (val[0], val[1], word_rate, meaning))
    nfile.close()


def main():
    #1. 读取文本
    words = read_files(get_file_from_folder('data1'))
   
    #2. 清洗文本
    f_words = format_words(words)
    total_word_count = len(f_words)

    #3. 统计单词和排序
    word_list = statictcs_words(f_words)

    start_and_end = [0.5, 0.7] 

    word_dict = read_dict("8000-words.txt")

    #4. 输出文件
    print_to_csv(word_list, word_dict, 'output/test.csv', total_word_count, start_and_end)

if __name__ == "__main__":
    main()