#!/usr/bin/env python
from __future__ import division, print_function

import argparse
import os
import re
import xml.etree.ElementTree as ET
from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_stuff(html):
    s = MLStripper()
    s.feed(html)
    return re.sub('[\t\n\r]', ' ', s.unescape(s.get_data()))


def parse_rec(dir, filename):
    measure_id = filename[:filename.find('xml') - 1]
    summary = ''
    numerator = ''
    denominator = ''

    tree = ET.parse(os.path.join(dir, filename))
    root = tree.getroot()

    for child in root.iter():
        if child.get('Name') == 'Brief Abstract':
            for rec in child:
                if rec.get('Name') in ['Description', 'Rationale']:
                    summary += strip_stuff(rec[0].get('Value'))
        elif child.get('Name') == 'Denominator Description':
            denominator = strip_stuff(child[0].get('Value'))
        elif child.get('Name') == 'Numerator Description':
            numerator = strip_stuff(child[0].get('Value'))
    return measure_id, summary, numerator, denominator


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'dump abstracts from measure xmls')
    parser.add_argument('source_dir', help='The directory containing the xml files')
    parser.add_argument('out_file', help='The output filename')

    args = parser.parse_args()

    with open(args.out_file, 'w') as ofile:
        for i, filename in enumerate(os.listdir(args.source_dir)):
            print('\r{} {}'.format(i, filename), end='\r')
            m, s, n, d = parse_rec(args.source_dir, filename)
            ofile.write(m + '\t' + s + ' ' + n + ' ' + d + '\n')
        print('\n')
