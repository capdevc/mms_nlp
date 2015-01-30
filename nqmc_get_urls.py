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

from splinter import Browser

links = []

with Browser('firefox',
             profile='/home/cc/.mozilla/firefox/0wnvf6xn.default') as browser:
    root_url = "http://www.qualitymeasures.ahrq.gov/browse/by-topic-detail.aspx?id=7814&ct=1"
    browser.visit(root_url)

    while True:
        link_objects = browser.find_link_by_partial_href('/content.aspx?id=')
        for link_object in link_objects:
            links.append(link_object['href'])
        if not browser.is_text_present('Next >'):
            break
        browser.find_link_by_text('Next >').first.click()

for link in links:
    print(link)