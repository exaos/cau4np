#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
Created on Thu Nov  9 10:15:24 2017

@author: exaos
"""
from __future__ import with_statement
from __future__ import absolute_import
from __future__ import print_function
import sys
if sys.version_info.major == 2:
    from io import open

import re


def read_mca(fm):
    u"""Purpose: Read data acquired by MCA8000A through software "pcma".
    Extention: .mca"""

    with open(fm, u"r") as fin:
        sraw = [l.strip() for l in fin.readlines()]

    if not sraw:
        return

    k_idx = []
    for i in range(len(sraw)):
        keys = re.findall(u'<<(.*)>>', sraw[i])
        if keys:
            k_idx.append([i, keys[0]])
    k_num = len(k_idx)
    if k_num < 3:
        print(u"WARNING: not a proper MCA spectrum!")

    spec = {}
    for k in range(k_num):
        i_start = k_idx[k][0] + 1
        if (k + 1) < k_num:
            i_end = k_idx[k + 1][0]
        else:
            i_end = -1

        # PMCA SPECTRUM
        if k_idx[k][1] == u'PMCA SPECTRUM':
            spec[u'INFO'] = dict()
            for l in sraw[i_start:i_end]:
                istr = [i.strip() for i in l.split(u'-')]
                if len(istr) > 1:
                    info_s = u"".join(istr[1:])
                    spec[u'INFO'][istr[0]] = eval(info_s) if \
                        info_s.isdigit() else info_s
                else:
                    print(u"WARNING: empty info key --", istr[0])

        # Calibration
        elif k_idx[k][1] == u'CALIBRATION':
            spec[u'CALI'] = dict()
            spec[u'CALI'][u'info'] = [
                i.strip() for i in sraw[i_start].split(u'-')
            ]
            if i_end != -1 and i_end <= i_start + 1:
                continue
            spec[u'CALI'][u'data'] = []
            for l in sraw[i_start + 1:i_end]:
                spec[u'CALI'][u'data'].append([eval(i) for i in l.split()])

        # ROI
        elif k_idx[k][1] == u'ROI':
            spec[u'ROI'] = []
            for l in sraw[i_start:i_end]:
                spec[u'ROI'].append([eval(i) for i in l.split()])

        # Data
        elif k_idx[k][1] == u'DATA':
            spec[u'DATA'] = [int(i) for i in sraw[i_start:i_end]]

        else:
            pass

    return spec


# The main
if __name__ == u'__main__':
    from pprint import pprint

    if len(sys.argv) < 2:
        print(u"Usage: {} <file.mca>".format(sys.argv[0]))
        sys.exit(0)

    spec = read_mca(sys.argv[1])
    if u'INFO' in spec:
        pprint(spec[u'INFO'])
