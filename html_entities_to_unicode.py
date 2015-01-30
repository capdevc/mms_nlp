'''
@uthor: Steven Keith Shook II
November 19, 2014

Purpose: Convert files that contain HTML Entities into Unicode characters.
'''

import os
import re


def convert_html_entities_to_unicode(filePath):
            line = line.replace("&amp;", "&")
            line = line.replace("&quot;", "\"")
            line = line.replace("&apos;", "'")
            line = line.replace("&lt;", "<")
            line = line.replace("&gt;", ">")

def remove_html_tags(line):
    p = re.compile(r'<.*?>')
    return p.sub('', line)


for filename in os.listdir('./data'):
    if not filename.startswith("."):
        filePath = './data/'+filename
        newFilePath = filePath[:-4] + "_clean" + filePath[-4:]
        with open(filePath, "U") as oldFile, open(newFilePath, "wb") as newFile:
            for idx, line in enumerate(oldFile):
                ##Put functions here to modify the lines in a file
                #line = convert_html_entities_to_unicode(line)
                line = remove_html_tags(line)

                newFile.write(str(line))