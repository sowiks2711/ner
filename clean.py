import codecs
import os
import re
from IPython.core.debugger import set_trace

def clean_and_save(path_rawfile, path_direction):
    f = codecs.open(path_rawfile, encoding='utf-8')
    l = list()
    for line in f:
        l.append(line)
    clean_document = re.sub( '<E(.{1,100})">', '' , l[0]) # ten przedzial dlatego, zeby usuwalo kolejne fragmenty, a nie duzy fragment tekstu
    clean_document = re.sub('</Entity>', '' , clean_document)
    f.close()
    f = codecs.open(path_direction, "w", encoding = 'utf-8')
    f.write(clean_document)
    f.close()

def clean_all_files(absolute_path_source, absolute_path_direction, dirs_list):
    for dirc in dirs_list:
        path_source = absolute_path_source + '\\' + dirc
        path_direction = absolute_path_direction + '\\' + dirc
        for file in os.listdir(path_source):
            clean_and_save(path_source + '\\' + file, path_direction + '\\' + file)
			
if __name__ == "__main__":
	absolute_path_source = 'C:\\Users\\piotr\\Desktop\\text\\TextMining\\learningData'
	absolute_path_direction = 'C:\\Users\\piotr\\Desktop\\text\\TextMining\\cleanData'
	dirs = ['korpusGAZETA', 'korpusONET']
	clean_all_files(absolute_path_source, absolute_path_direction, dirs)