#!/usr/bin/env python
from __future__ import division, print_function
'''
@uthor: Steven Keith Shook II
November 19, 2014

Purpose: Download files from a website.

Problem:

Splinter Library Docs
https://splinter.readthedocs.org/en/latest/

'''

import sys
import time
from splinter import Browser


with Browser('firefox',
             profile='/home/cc/.mozilla/firefox/0wnvf6xn.default') as browser:
    for url in sys.stdin:
        browser.visit(url)
        download_link = browser.find_by_id('ctl00_ContentPlaceHolder1_lbXMLDownload')
        download_link.click()
        time.sleep(1)
