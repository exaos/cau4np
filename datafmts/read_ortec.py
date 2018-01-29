#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 01:52:02 2017

@author: exaos
"""

from __future__ import with_statement
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from builtins import open
from builtins import int
from future import standard_library
standard_library.install_aliases()
import sys
from struct import unpack, calcsize
from ctypes import c_char_p
from datetime import date, timedelta, datetime
import numpy as np


def get_month_num(mn):
    """Map month name to number."""

    return {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12
    }.get(mn, 0)


def format_ortec_time(bsec, btime, bdate, is_paced=True):
    """Format ORTEC time as ISO format: yyyy-mm-dd HH:MM."""

    tSS = int(bsec) if bsec != b'\x00\x00' else 0
    tHH = int(btime[:2])
    tMM = int(btime[3:5]) if is_paced else int(btime[2:4])
    dd = int(bdate[:2])
    b_mon = bdate[3:6] if is_paced else bdate[2:5]
    mm = get_month_num(b_mon.decode().lower())
    yy = int(bdate[7:9]) if is_paced else int(bdate[5:7])
    yy += 2000 if bdate.endswith(b'1') else 1900

    return datetime(yy, mm, dd, tHH, tMM, tSS)


############################################################

def parse_ortec_chn_tail(ss):
    """Parse the tail info in ORTEC integer data spectrum file."""

    assert (len(ss) >= 512), u"Bad tail record"

    # Spec type: -101 or -102
    s_type = unpack("<1h 2x", ss[:4])[0]

    # Calibration info
    d_cali = unpack("<6f 228x", ss[4:256])
    # d_cali = unpack("<2f4x2f232x", ss[4:256])
    cali = {
        'energy': {'zero-intercept': d_cali[0], 'slope': d_cali[1]},
        'peak': {'zero-intercept': d_cali[2], 'slope': d_cali[4]},
    }
    if s_type == -102:
        cali['energy']['quadratic'] = d_cali[3]
        cali['peak']['quadratic'] = d_cali[5]

    # Descriptions
    d_desc = unpack("<1b 63s 1b 63s", ss[256:384])
    desc = {
        "detector": [d_desc[0], c_char_p(d_desc[1]).value.decode()],
        "sample": [d_desc[2], c_char_p(d_desc[3]).value.decode()]
    }

    # for Old AlphaVision version
    misc = {"desc": desc, }
    if s_type == -101:
        misc['chn_type'] = u"Early Versions"
    else:
        if s_type == -102 and unpack("<1I", ss[384:388]) == 0x53495641:
            misc['chn_type'] = u"Old AlphaVision version"
            # ss[388:512], the Old AlphaVision info
            misc["rAlphaVision"] = unpack("<32s 10s 10s 3f1h7f 30s", ss[388:])
        else:
            misc['chn_type'] = u"New Versions"

    return {
        'detector': desc['detector'][1],
        'sample': desc['sample'][1],
        'misc': misc,
        'cali': cali,
    }


def parse_ortec_chn(fin):
    u"""Parse ORTEC integer data spectrum file (*.chn).

    Ref: File structure manual, pp.5
    """
    # Read HEADER

    fmt_h = "<3h 2s 2i 8s 4s 2h"
    h_raw = unpack(fmt_h, fin.read(calcsize(fmt_h)))
    assert h_raw[0] == -1

    start_time = format_ortec_time(h_raw[3], h_raw[7], h_raw[6], False)
    data = {"dtype": "i16", "dlen": h_raw[9]}
    info_acq = {
        'time': {
            'start': {'sec': start_time.timestamp(), 'nsec': 0.0},
            'stop': {'sec': 0.0, 'nsec': 0.0},
            'real': float(h_raw[4]) * 0.020,
            'live': float(h_raw[5]) * 0.020,
        },
        'device': {'id': h_raw[1], 'name': "MCA", },
        'original': {
            'filename': fin.name,
            'filetype': "ORTEC Integer Data (.chn)"
        }}
    info_op = {}
    info_misc = {"det_num": h_raw[2], "offset": h_raw[8]}
    # info_misc['start_time'] = start_time.isoformat()

    # Read DATA

    fmt_d = "<{}i".format(data['dlen'])
    d_in = fin.read(calcsize(fmt_d))

    data['dset'] = np.array(unpack(fmt_d, d_in), dtype=np.int16)

    # Read Tail

    info_r = parse_ortec_chn_tail(fin.read(512))
    info_op['detector'] = info_r['detector']
    info_op['sample'] = info_r['sample']
    info_cali = info_r['cali']
    info_misc.update(info_r['misc'])

    return {
        'data': data,
        'info-acq': info_acq,
        'info-op': info_op,
        'info-cali': info_cali,
        'info-misc': info_misc,
    }


def read_ortec_chn(fn):
    """Read ORTEC integer data spectrum file (*.chn)."""

    with open(fn, u"rb") as fin:
        return parse_ortec_chn(fin)


############################################################

def parse_ortec_spc_header(ss):
    """Parse 1st record in .spc file."""

    assert (len(ss) >= 128), u"Bad 1st record"

    # File type and flags
    r_types = unpack("<3h2x", ss[:8])
    assert r_types[0] == 1
    spc_type, spc_type_desc, is_real = {
        1: (1, "ORTEC Integer Spectrum", False),
        5: (2, "ORTEC Real Spectrum", True),
        7: (3, "ORTEC Real Net Spectrum", True),
        3: (3, "ORTEC Integer Net Spectrum", False)
    }.get(r_types[1], Exception("Bad file format!"))
    # Long filename or not
    is_long_filename = (r_types[2] & 0b01) == 1
    # Is ZDT with ROI?
    is_zdt_with_roi = (r_types[2] & 0b10) == 0b10

    # ss[8:40] -- various pointers
    pointers = unpack("<16h", ss[8:40])

    # ss[40:54] -- pointers to ROI records, etc.

    # ss[54:60] -- various numbers

    # ss[60:68] -- to calculate spectrum data pointer and length
    r_spcdata = unpack("<3h", ss[60:66])

    # ss[68:80] -- acquisition time
    r_acqtime = unpack("<1f 1d", ss[68:80])

    # ss[86:98] -- mca, start_chn, real/live time
    r_rec = unpack("<2h 2f", ss[86:98])

    return {
        "spc_type": spc_type_desc,
        "is_real": is_real,
        "is_long_filename": is_long_filename,
        "is_zdt_with_roi": is_zdt_with_roi,
        "spc_data_pos": r_spcdata[0],
        "spc_data_blocks": r_spcdata[1],
        "spc_num_of_chns": r_spcdata[2],
        "acq_datetime": date(1979, 1, 1) + timedelta(r_acqtime[1]),
        "real_time": r_rec[2],
        "live_time": r_rec[3],
        "mca_dev_type": r_rec[0],
        "start_chn_num": r_rec[1],
        "ptrs": pointers,
    }


def parse_ortec_acq_info(ss):
    """Parse acquisition information record(block)."""

    assert len(ss) == 128

    r = unpack("<16s 12s 10s 10s 10s 34x 10s 8s 10s 8s", ss)

    return {
        "default_filename": r[0].decode().strip(),
        "datetime": format_ortec_time(r[2][6:8], r[2][:5], r[1][:10]),
        "live_time_rounded": int(r[3]),
        "real_time_rounded": int(r[4]),
        "start_time": format_ortec_time(r[6][6:8], r[6][:5], r[5][:10]),
        "stop_time": format_ortec_time(r[8][6:8], r[8][:5], r[7][:10]),
    }


def parse_ortec_spc(fin):
    """
    Parse ORTEC spectrum file (*.spc).

    Ref: File structure manual,
      1. real format -- sec.4.11, pp.29
      2. integer format -- sec.4.12, pp.41
      3. net spectrum -- sec.4.13, pp.43

    Record 1~16: pp.29~41.
    """

    # parse header (1st record)

    h = parse_ortec_spc_header(fin.read(128))

    # parse acquisition information
    acq_info_pos = (h["ptrs"][0]-1)*128
    fin.seek(acq_info_pos)
    acq = parse_ortec_acq_info(fin.read(128))

    # parse data

    d_pos = (h["spc_data_pos"] - 1)*128
    d_len = h["spc_num_of_chns"]*4
    assert d_len <= (h["spc_data_blocks"]*128)
    fin.seek(d_pos)
    b_data = fin.read(d_len)
    d_len_r = len(b_data)
    d_fmt = "<{}{}".format(h["spc_num_of_chns"], "f" if h["is_real"] else "i")
    assert (d_len_r == d_len), "Data length: {0} !={1}".format(d_len_r, d_len)
    darr = unpack(d_fmt, b_data)

    # format dicts

    dt_s, dt_np = ("f32", np.float32) if h["is_real"] else ("i32", np.int32)
    data = {
        "dtype": dt_s,
        "dlen": h["spc_num_of_chns"],
        "dset": np.array(darr, dt_np)}
    info_acq = {
        "time": {
            "start": {"sec": acq['start_time'].timestamp(), "nsec": 0.0},
            "stop": {"sec": acq['stop_time'].timestamp(), "nsec": 0.0},
            "real": h['real_time'],
            "live": h['live_time'],
        },
        "original": {
            "filename": acq['default_filename'],
            "filetype": h['spc_type'],
        }}

    return {"data": data, "info-acq": info_acq, "header": h}


def parse_ortec_lib_header(ss):
    """
    Parse LIBRARY file header. (Sec.6.1, pp.75-76)
    """

    assert len(ss) == 128

    fmt_h = "<6h 4x 16h 16x 18s 2x 18s 2h 22x"
    r = unpack(fmt_h, ss)

    return {
        "raw": r
    }


def parse_ortec_lib_nuclide(ss):
    """
    Parse nuclde records in library file.
    Sec.6.1.2, pp.76-77

    Each record is 21-words (42-bytes) long.
    """

    assert len(ss) == 42

    fmt_s = "<8s 2f 4h 8x 1h 2x 3h"
    r = unpack(fmt_s, ss)

    return {
        "raw": r
    }


def parse_ortec_lib_peak(ss):
    """
    Parse peak records in library file. (Sec.6.1.3, pp.77)

    Each record is 16-words (32-bytes) long.
    """

    assert len(ss) == 32

    fmt_s = "<2f 1h 6x 2h 4x 4h"
    r = unpack(fmt_s, ss)

    return {
        "raw": r
    }


############################################################


def read_ortec_spc(fn):
    """Read ORTEC spectrum file (*.spc)."""

    with open(fn, "rb") as fin:
        return parse_ortec_spc(fin)


def read_ortec_lib(fn):
    """Read ORTEC library file (.lib).

    Ref: File structure manual
      1. Library files (Ge) -- sec 6.1, pp.75
    """

    print(u"Not implemented!")


def read_ortec_roi(fn):
    """Read ORTEC spectrum .roi files (*.roi).

    File format:
        1h : must be -2
        1h : Start channel number of first ROI
        1h : Stop cahnnel number of first ROI
        ...
        -  : Continue for all ROIs in the display
        1h : Start channel = -1 is end of data.
    """

    print(u"Not implemented!")


def read_ortec_prm(fn):
    """
    Read ORTEC analysis parameter files (*.prm).
    Ref: File structure manual, pp.9
    """

    print(u"Not implemented!")


def read_ortec_clb(fn):
    """Read ORTEC calibration files (*.clb).
    Ref: File structure manual, pp.17
    """

    print(u"Not implemented!")


def read_ortec_det(fn):
    """
    Read ORTEC detector description files (*.det).
    Ref: File structure manual, pp.23
    """

    print(u"Not implemented!")


def read_ortec_smp(fn):
    """
    Read ORTEC sample description files (*.smp).
    Ref: File structure manual, pp.26
    """

    print(u"Not implemented!")


############################################################

def read_ortec(fn):
    """
    Read spectrum file by ORTEC
    (*.chn/.spc/.roi/.prm/.clb/.det/.smp/.lib).
    """

    return {
        ".chn": read_ortec_chn,
        ".spc": read_ortec_spc,
        ".roi": read_ortec_roi,
        ".prm": read_ortec_prm,
        ".clb": read_ortec_clb,
        ".det": read_ortec_det,
        ".smp": read_ortec_smp,
        ".lib": read_ortec_lib
    }.get(fn[-4:].lower())(fn)


############################################################


if __name__ == '__main__':
    from pprint import pprint

    if (len(sys.argv)) < 2:
        print(u"Usage: {} <file.[chn|spc]>".format(sys.argv[0]))
        sys.exit(0)

    spec = read_ortec(sys.argv[1])
    for k in spec:
        print(k, ":")
        pprint(spec[k], compact=True)
