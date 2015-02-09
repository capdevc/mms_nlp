#!/usr/bin/env python
from __future__ import division, print_function

import sys
from lxml import etree


pmid, text = (None, None)
for x, element in etree.iterparse(sys.stdin, events=('start', 'end')):
    if element.tag == 'PubmedArticle':
        if pmid and text:
            sys.stdout.write(pmid + "\t" + text + "\n")
        pmid, text = (None, None)
    elif element.tag == 'PMID':
        pmid = element.text
    elif element.tag == 'AbstractText':
        text = element.text
