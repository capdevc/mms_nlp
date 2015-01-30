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


def parse_rec(filename):
    at = ''
    tree = ET.parse(filename)
    root = tree.getroot()

    for child in root.iter():
        if child.get('Name') == 'Brief Abstract':
            for rec in child:
                if rec.get('Name') in ['Description', 'Rationale']:
                    at += strip_stuff(rec[0].get('Value'))
        elif child.get('Name') == 'Denominator Description':
            at += (' ' + strip_stuff(child[0].get('Value')))
        elif child.get('Name') == 'Numerator Description':
            at += (' ' + strip_stuff(child[0].get('Value')))
    return at


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert measure downloader' +
                                     ' xml files to plain text abstracts.')
    parser.add_argument('directory', help='The directory containing measure' +
                        ' xml files.')
    args = parser.parse_args()
    path = args.directory
    for i, filename in enumerate(os.listdir(path)):
        at = parse_rec(os.path.join(path, filename))
        if at is not '':
            print(at)
