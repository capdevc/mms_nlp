#!/usr/bin/env python
from __future__ import division, print_function
import requests
import sys


eutils_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi'
basic_params = [('tool', 'medic'),
                ('db', 'pubmed'),
                ('retmode', 'xml'),
                ('rettype', 'medline')]

pmid_list = []
for line in sys.stdin:
    chunks = line.strip().split('\t')
    pmid_list += (chunks[4].split(',') + chunks[5].split(','))

pmids = set(pmid_list)
if '0' in pmids:
    pmids.remove('0')

params = reduce(lambda x, y: x + [('id', y)],
                pmids, basic_params)

response = requests.post(eutils_url, params)
sys.stdout.write(response.text.encode('ascii', 'ignore'))
