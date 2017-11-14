#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u"""
Created on Thu Nov 19 01:52:02 2017

@author: exaos
"""

from __future__ import with_statement
from __future__ import absolute_import
from __future__ import print_function
from struct import unpack, calcsize
from ctypes import c_char_p
from datetime import date, timedelta, datetime
import sys
if sys.version_info.major == 2:
    from io import open


def get_month_num(mn):
    u"""Map month name to number."""

    return {u"jan": 1,
            u"feb": 2,
            u"mar": 3,
            u"apr": 4,
            u"may": 5,
            u"jun": 6,
            u"jul": 7,
            u"aug": 8,
            u"sep": 9,
            u"oct": 10,
            u"nov": 11,
            u"dec": 12}.get(mn, 0)


def format_ortec_time(bsec, btime, bdate, is_paced=True):
    u"""Format ORTEC time as ISO format: yyyy-mm-dd HH:MM."""

    tSS = int(bsec) if bsec != '\x00\x00' else 0
    tHH = int(btime[:2])
    tMM = int(btime[3:5]) if is_paced else int(btime[2:4])
    dd = int(bdate[:2])
    b_mon = bdate[3:6] if is_paced else bdate[2:5]
    mm = get_month_num(b_mon.decode().lower())
    yy = int(bdate[7:9]) if is_paced else int(bdate[6:8])
    yy += 2000 if bdate.endswith(b'1') else 1900

    return datetime(yy, mm, dd, tHH, tMM, tSS).isoformat(" ")


############################################################

def parse_ortec_chn_tail(ss):
    u"""Parse the tail info in ORTEC integer data spectrum file."""

    assert (len(ss) >= 512), u"Bad tail record"

    # Spec type: -101 or -102
    s_type = unpack(u"<1h 2x", ss[:4])[0]

    # Calibration info
    d_cali = unpack(u"<6f 228x", ss[4:256])
    # d_cali = unpack("<2f4x2f232x", ss[4:256])
    cali = {u"eng_zero_intercept": d_cali[0], u"eng_slope": d_cali[1],
            u"peak_shape_zero_intercept": d_cali[3],
            u"peak_shape_slope": d_cali[4]}
    if s_type == -102:
        cali[u"eng_quadratic_term"] = d_cali[3]
        cali[u"peak_shape_quadratic_term"] = d_cali[5]

    # Descriptions
    d_desc = unpack(u"<1b 63s 1b 63s", ss[256:384])
    desc = {u"detector": [d_desc[0], c_char_p(d_desc[1]).value.decode()],
            u"sample": [d_desc[2], c_char_p(d_desc[3]).value.decode()]}

    # for Old AlphaVision version
    if s_type == -101:
        chn_type = u"Early Versions"
    else:
        if s_type == -102 and unpack(u"<1I", ss[384:388]) == 0x53495641:
            chn_type = u"Old AlphaVision version"
            # ss[388:512], the Old AlphaVision info
            desc[u"rAlphaVision"] = unpack(u"<32s 10s 10s 3f1h7f 30s", ss[388:])
        else:
            chn_type = u"New Versions"

    return {
        u"chn_type": chn_type,
        u"descriptions": desc,
        u"calibrations": cali
    }


def parse_ortec_chn(fin):
    u"""Parse ORTEC integer data spectrum file (*.chn).

    Ref: File structure manual, pp.5
    """
    # Read HEADER

    fmt_h = u"<3h 2s 2i 8s 4s 2h"
    h_raw = unpack(fmt_h, fin.read(calcsize(fmt_h)))
    assert h_raw[0] == -1

    head = {
        u"num_MCA": h_raw[1],
        u"num_DET": h_raw[2],
        u"acq_real_time": float(h_raw[4]) * 0.020,
        u"acq_live_time": float(h_raw[5]) * 0.020,
        # change start date_time to iso format
        u"start_time": format_ortec_time(h_raw[3], h_raw[7], h_raw[6], False),
        u"offset": h_raw[8],
        u"channel_length": h_raw[9]
    }

    # Read DATA

    fmt_d = u"<{}i".format(head[u"channel_length"])
    d_in = fin.read(calcsize(fmt_d))

    data = unpack(fmt_d, d_in)

    # Read Tail

    info = parse_ortec_chn_tail(fin.read(512))

    return {
        u"header": head,
        u"data": data,
        u"info": info
    }


def read_ortec_chn(fn):
    u"""Read ORTEC integer data spectrum file (*.chn)."""

    with open(fn, u"rb") as fin:
        return parse_ortec_chn(fin)


############################################################

def parse_ortec_spc_header(ss):
    u"""Parse 1st record in .spc file."""

    assert (len(ss) >= 128), u"Bad 1st record"

    # File type and flags
    r_types = unpack(u"<3h2x", ss[:8])
    assert r_types[0] == 1
    spc_type, spc_type_desc, is_real = {
        1: (1, u"Integer Spectrum", False),
        5: (2, u"Real Spectrum", True),
        7: (3, u"Real Net Spectrum", True),
        3: (3, u"Integer Net Spectrum", False)
    }.get(r_types[1], Exception(u"Bad file format!"))
    # Long filename or not
    is_long_filename = (r_types[2] & 0b01) == 1    
    # Is ZDT with ROI?
    is_zdt_with_roi = (r_types[2] & 0b10) == 0b10

    # ss[8:40] -- various pointers
    pointers = unpack(u"<16h", ss[8:40])

    # ss[40:54] -- pointers to ROI records, etc.

    # ss[54:60] -- various numbers

    # ss[60:68] -- to calculate spectrum data pointer and length
    r_spcdata = unpack(u"<3h", ss[60:66])

    # ss[68:80] -- acquisition time
    r_acqtime = unpack(u"<1f 1d", ss[68:80])

    # ss[86:98] -- mca, start_chn, real/live time
    r_rec = unpack(u"<2h 2f", ss[86:98])

    return {
        u"spec_type": spc_type_desc,
        u"is_real": is_real,
        u"is_long_filename": is_long_filename,
        u"is_zdt_with_roi": is_zdt_with_roi,
        u"spc_data_pos": r_spcdata[0],
        u"spc_data_blocks": r_spcdata[1],
        u"spc_num_of_chns": r_spcdata[2],
        u"acq_datetime": date(1979, 1, 1) + timedelta(r_acqtime[1]),
        u"real_time": r_rec[2],
        u"live_time": r_rec[3],
        u"mca_dev_type": r_rec[0],
        u"start_chn_num": r_rec[1],
        u"ptrs": pointers
    }


def parse_ortec_acq_info(ss):
    u"""Parse acquisition information record(block)."""

    assert len(ss) == 128

    r = unpack(u"<16s 12s 10s 10s 10s 34x 10s 8s 10s 8s", ss)

    return {
        u"default_filename": r[0].decode().strip(),
        u"datetime": format_ortec_time(r[2][6:8], r[2][:5], r[1][:10]),
        u"live_time_rounded": int(r[3]),
        u"real_time_rounded": int(r[4]),
        u"start_time": format_ortec_time(r[6][6:8], r[6][:5], r[5][:10]),
        u"stop_time": format_ortec_time(r[8][6:8], r[8][:5], r[7][:10]),
    }


def parse_ortec_spc(fin):
    u"""Parse ORTEC spectrum file (*.spc).

    Ref: File structure manual,
      1. real format -- sec.4.11, pp.29
      2. integer format -- sec.4.12, pp.41
      3. net spectrum -- sec.4.13, pp.43

    Record 1~16: pp.29~41.
    """

    # parse header (1st record)

    h = parse_ortec_spc_header(fin.read(128))

    # parse acquisition information
    acq_info_pos = (h[u"ptrs"][0]-1)*128
    fin.seek(acq_info_pos)
    acq = parse_ortec_acq_info(fin.read(128))
    h.update(acq)

    # parse data

    d_pos = (h[u"spc_data_pos"] - 1)*128
    d_len = h[u"spc_num_of_chns"]*4
    assert d_len <= (h[u"spc_data_blocks"]*128)
    fin.seek(d_pos)
    b_data = fin.read(d_len)
    d_len_r = len(b_data)
    d_fmt = u"<{}{}".format(h[u"spc_num_of_chns"], u"f" if h[u"is_real"] else u"i")
    assert (d_len_r == d_len), u"Data length: {0} !={1}".format(d_len_r, d_len)
    data = unpack(d_fmt, b_data)

    return {
        u"header": h,
        u"data": data
    }


def parse_ortec_lib_header(ss):
    u"""Parse LIBRARY file header.
    Sec.6.1, pp.75-76"""

    assert len(ss) == 128

    fmt_h = u"<6h 4x 16h 16x 18s 2x 18s 2h 22x"
    r = unpack(fmt_h, ss)

    return {
        u"raw": r
    }


def parse_ortec_lib_nuclide(ss):
    u"""Parse nuclde records in library file.
    Sec.6.1.2, pp.76-77

    Each record is 21-words (42-bytes) long."""

    assert len(ss) == 42

    fmt_s = u"<8s 2f 4h 8x 1h 2x 3h"
    r = unpack(fmt_s, ss)

    return {
        u"raw": r
    }


def parse_ortec_lib_peak(ss):
    u"""Parse peak records in library file.
    Sec.6.1.3, pp.77

    Each record is 16-words (32-bytes) long."""

    assert len(ss) == 32

    fmt_s = u"<2f 1h 6x 2h 4x 4h"
    r = unpack(fmt_s, ss)

    return {
        u"raw": r
    }


############################################################


def read_ortec_spc(fn):
    u"""Read ORTEC spectrum file (*.spc)."""

    with open(fn, u"rb") as fin:
        return parse_ortec_spc(fin)


def read_ortec_lib(fn):
    u"""Read ORTEC library file (.lib).

    Ref: File structure manual
      1. Library files (Ge) -- sec 6.1, pp.75
    """

    print(u"Not implemented!")


def read_ortec_roi(fn):
    u"""Read ORTEC spectrum .roi files (*.roi).

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
    u"""Read ORTEC analysis parameter files (*.prm).

    Ref: File structure manual, pp.9"""

    print(u"Not implemented!")


def read_ortec_clb(fn):
    u"""Read ORTEC calibration files (*.clb).

    Ref: File structure manual, pp.17"""

    print(u"Not implemented!")


def read_ortec_det(fn):
    u"""Read ORTEC detector description files (*.det).

    Ref: File structure manual, pp.23"""

    print(u"Not implemented!")


def read_ortec_smp(fn):
    u"""Read ORTEC sample description files (*.smp).

    Ref: File structure manual, pp.26"""

    print(u"Not implemented!")


############################################################

def read_ortec(fn):
    u"""Read spectrum file by ORTEC
    (*.chn/.spc/.roi/.prm/.clb/.det/.smp/.lib).
    """

    return {
        u".chn": read_ortec_chn,
        u".spc": read_ortec_spc,
        u".roi": read_ortec_roi,
        u".prm": read_ortec_prm,
        u".clb": read_ortec_clb,
        u".det": read_ortec_det,
        u".smp": read_ortec_smp,
        u".lib": read_ortec_lib
    }.get(fn[-4:].lower())(fn)


############################################################


if __name__ == '__main__':
    from pprint import pprint

    if (len(sys.argv)) < 2:
        print(u"Usage: {} <file.[chn|spc]>".format(sys.argv[0]))
        sys.exit(0)

    spec = read_ortec(sys.argv[1])
    if u'header' in spec:
        pprint(spec[u'header'])

