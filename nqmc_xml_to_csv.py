#!/usr/bin/env python
from __future__ import division, print_function


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
    measure_id = filename[:filename.find("xml") - 1]
    summary = ""
    numerator = ""
    denominator = ""
    source_ids = list()
    evidence_ids = list()

    tree = ET.parse("cardio/" + filename)
    root = tree.getroot()

    for child in root.iter():
        if child.get("Name") == "Brief Abstract":
            for rec in child:
                if rec.get("Name") in ["Description", "Rationale"]:
                    summary += strip_stuff(rec[0].get("Value"))
        elif child.get("Name") == "Denominator Description":
            denominator = strip_stuff(child[0].get("Value"))
        elif child.get("Name") == "Numerator Description":
            numerator = strip_stuff(child[0].get("Value"))
        elif child.get("Type") == ("citation" and "source"
                                   in child.get("Name").lower()):
            for rec in child:
                if "list_uids" in rec.get("Value"):
                    m = re.search(r"list_uids=(\d+)\"", rec.get("Value"))
                    source_ids.append(m.group(1))
        elif child.get("Type") == ("citation" and "evidence"
                                   in child.get("Name").lower()):
            for rec in child:
                if "list_uids" in rec.get("Value"):
                    m = re.search(r"list_uids=(\d+)\"", rec.get("Value"))
                    evidence_ids.append(m.group(1))
    return measure_id, summary, numerator,\
        denominator, source_ids, evidence_ids


with open("cardio_measures.csv", "w") as ofile:
    for i, filename in enumerate(os.listdir(os.getcwd() + "/cardio/")):
        print(i, filename)
        m, s, n, d, si, ei = parse_rec(filename)
        st = "0" if not si else ",".join(si)
        et = "0" if not ei else ",".join(ei)
        ofile.write(m + "\t" + s + "\t" + n + "\t" + d +
                    "\t" + st + "\t" + et + "\n")