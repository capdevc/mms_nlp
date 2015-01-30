#!/usr/bin/env python
from __future__ import division, print_function

import sys
from lxml import etree


for x, element in etree.iterparse(sys.stdin, tag='AbstractText'):
    if element.tag == 'AbstractText':
        print(element.text)
