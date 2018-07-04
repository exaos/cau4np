#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
Created on Thu Nov  9 10:15:24 2017

@author: exaos
"""
from __future__ import with_statement
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from builtins import range
from builtins import open
from builtins import dict
from builtins import int
from future import standard_library
standard_library.install_aliases()
import sys
import re
from datetime import datetime


def parse_pmca_str(sraw):
    """Parse MCA data in text."""

    k_idx = []
    for i in range(len(sraw)):
        keys = re.findall(r'<<(.*)>>', sraw[i])
        if keys:
            k_idx.append([i, keys[0]])
    k_num = len(k_idx)
    if k_num < 3:
        print("WARNING: not a proper MCA spectrum!")

    spec = {}
    for k in range(k_num):
        i_start = k_idx[k][0] + 1
        if (k + 1) < k_num:
            i_end = k_idx[k + 1][0]
        else:
            i_end = -1

        # PMCA SPECTRUM
        if k_idx[k][1] == u'PMCA SPECTRUM':
            spec['INFO'] = dict()
            for l in sraw[i_start:i_end]:
                istr = [i.strip() for i in l.split(u'-')]
                if len(istr) > 1:
                    info_s = u"".join(istr[1:])
                    spec['INFO'][istr[0]] = eval(info_s) if \
                        info_s.isdigit() else info_s
                else:
                    print(u"WARNING: empty info key --", istr[0])

        # Calibration
        elif k_idx[k][1] == u'CALIBRATION':
            spec['CALI'] = dict()
            spec['CALI'][u'info'] = [
                i.strip() for i in sraw[i_start].split(u'-')
            ]
            if i_end != -1 and i_end <= i_start + 1:
                continue
            spec['CALI'][u'data'] = []
            for l in sraw[i_start + 1:i_end]:
                spec['CALI'][u'data'].append([eval(i) for i in l.split()])

        # ROI
        elif k_idx[k][1] == u'ROI':
            spec['ROI'] = []
            for l in sraw[i_start:i_end]:
                spec['ROI'].append([eval(i) for i in l.split()])

        # Data
        elif k_idx[k][1] == u'DATA':
            spec['DATA'] = [int(i) for i in sraw[i_start:i_end]]

        else:
            pass

    return reformat_pmca_spec(spec)


def reformat_pmca_spec(spec):
    '''
    Re-format spectrum.
    '''
    def tstr_to_sec(tstr):
        try:
            dt = datetime.strptime(tstr, '%m/%d/%Y %H:%M:%S').timestamp()
        except:
            dt = 0.0
        finally:
            return dt

    data = {}
    if 'DATA' in spec:
        data['dtype'] = 'i32'
        data['dlen'] = len(spec['DATA'])
        data['dset'] = spec.pop('DATA')
    info_acq = {'time': {}, 'device': {}, 'original': {}}
    info_op = {}
    info_ana = {}
    info_cali = {}
    info_misc = {}
    if 'INFO' in spec:
        if 'START_TIME' in spec['INFO']:
            info_acq['time']['start'] = {
                'sec': tstr_to_sec(spec['INFO'].pop('START_TIME')),
                'nsec': 0.0}
        if 'LIVE_TIME' in spec['INFO']:
            info_acq['time']['live'] = float(spec['INFO'].pop('LIVE_TIME'))
        if 'REAL_TIME' in spec['INFO']:
            info_acq['time']['real'] = float(spec['INFO'].pop('REAL_TIME'))
        if 'TAG' in spec['INFO']:
            info_op['sample'] = spec['INFO'].pop('TAG')
        if 'DESCRIPTION' in spec['INFO']:
            info_op['description'] = spec['INFO'].pop('DESCRIPTION')
        info_misc.update(spec['INFO'])
    if 'CALIBRATION' in spec:
        info_cali['energy'] = {}
        r_cali = spec.pop('CALI')
        if 'data' in r_cali:
            info_cali['energy']['points'] = r_cali['data']
    if 'ROI' in spec:
        info_ana['roi'] = spec.pop('ROI')

    return {'data': data,
            'info_acq': info_acq,
            'info_op': info_op,
            'info_ana': info_ana,
            'info_cali': info_cali,
            'info_misc': info_misc}


def dump_pmca(fm):
    """
    Purpose: Read data acquired by MCA8000A through software "pmca".
    Extention: .mca
    """

    with open(fm, "r") as fin:
        sraw = [l.strip() for l in fin.readlines()]
        assert sraw is not []

    return parse_pmca_str(sraw)


# The main
if __name__ == '__main__':
    from pprint import pprint

    if len(sys.argv) < 2:
        print(u"Usage: {} <file.mca>".format(sys.argv[0]))
        sys.exit(0)

    spec = dump_pmca(sys.argv[1])
    pprint(spec, compact=True)
