#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Parsing data saved by Tektronix TDS3034.
@Exaos
'''

import os
from struct import unpack, calcsize
import numpy as np
import h5py
import hdfdict


def _tek_tds3000_isf_header_dict(str_h):
    hd = {}
    for j in str_h.split(";"):
        l = j.split(' ')
        k = l[0].replace(":", "_")
        v = " ".join(l[1:]).replace('"', '').replace('#', '')
        if v.isnumeric():
            hd[k] = int(v, 10)
        else:
            try:
                hd[k] = float(v)
            except:
                hd[k] = v
    return hd


def _tek_tds3000_isf_get_header(raw_s):
    try:
        assert type(raw_s) == bytes
        pos = raw_s.find(b'CURVE #')
        digi_x = int(raw_s[pos + 7 : pos + 8].decode("ascii"))
        hd_len = pos + 8 + digi_x
        rec_len = int(raw_s[pos + 8 : hd_len].decode("ascii"))
        raw = raw_s[:hd_len].decode("ascii", "ignore")
        hd = _tek_tds3000_isf_header_dict(raw)
        hd["_digi_x"] = digi_x
        hd["_rec_len"] = rec_len
        hd["_hd_len"] = hd_len
        return hd
    except:
        return None


wave_dtype = np.dtype([("time", np.float32), ("volt", np.float32)])


def parse_tds3000_isf(fn):
    hd = {}
    with open(fn, "rb") as f:
        hd.update(_tek_tds3000_isf_get_header(f.read(512)))
        # seek the starting position of binary data
        f.seek(hd["_hd_len"])
        d_byte_order = {"LSB": "<", "MSB": ">"}.get(hd["BYT_OR"])
        d_type = {1:"c", 2:"h", 4:"i", 8:"l"}.get(hd["BIT_NR"]/8)
        dat_str = "{}{}{}".format(d_byte_order, hd["NR_PT"], d_type)
        assert calcsize(dat_str) == hd["_rec_len"]
        dat = unpack(dat_str, f.read(hd["_rec_len"]))
        hd['wave'] = np.array(
            [(hd['XZERO'] + hd['XINCR'] * (j - hd["PT_OFF"]),
              hd['YZERO'] + hd['YMULT'] * (float(dat[j]) - hd["YOFF"]))
             for j in range(hd["NR_PT"])],
            dtype=wave_dtype)
    return hd


def _dump_tds3000_isf_to_hdf5(fn, f5grp):
    print("Processing {} ...".format(fn))
    hd = parse_tds3000_isf(fn)
    wave = hd.pop('wave')
    hdfdict.dump(hd, f5grp)
    f5grp.create_dataset("waveform", (hd['NR_PT'],),
                         dtype=wave_dtype, data=wave,
                         compression=9, chunks=True)


def dump_tds3000_isf_to_hdf5(fn, fout=None):
    if not fout:
        fout = fn[:-4] + '-isf.h5'
    f5 = h5py.File(fout, "w")
    _dump_tds3000_isf_to_hdf5(fn, f5)
    f5.close()


def _get_isf_list(fdir):
    isf_l = []
    for root, folders, files in os.walk(fdir):
        for fn in files:
            if fn.lower().endswith(".isf"):
                full_fn = os.path.join(root, fn)
                f_id = full_fn[:-4].replace("/", "_")
                isf_l.append([f_id, full_fn, fn])
    return isf_l


def _dump_tds3000_isf_in_dir(fdir, f5grp=None):
    for _fi in _get_isf_list(fdir):
        if f5grp:
            grp = f5grp.create_group(_fi[0])
            _dump_tds3000_isf_to_hdf5(_fi[1], grp)
        else:
            dump_tds3000_isf_to_hdf5(_fi[1])


def dump_tds3000_isf_in_dir(fdir, fout=None):
    f5 = h5py.File(fout, "w") if fout else None
    _dump_tds3000_isf_in_dir(fdir, f5grp=f5)
    if f5:
        f5.close()


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Example")
    parser.add_argument("-o", "--output", action='store', dest='output')
    parser.add_argument("name", nargs="*")

    nsp = parser.parse_args()
    if "name" in nsp and nsp.name:
        f5 = None
        if "output" in nsp and nsp.output:
            f5 = h5py.File(nsp.output, "w")
        for fn in nsp.name:
            if os.path.isdir(fn):
                _dump_tds3000_isf_in_dir(fn, f5grp=f5)
            elif os.path.isfile(fn) and fn.lower().endswith(".isf"):
                if f5:
                    grp = f5.create_group(fn[:-4].replace("/", "_"))
                    _dump_tds3000_isf_to_hdf5(fn, grp)
                else:
                    dump_tds3000_isf_to_hdf5(fn)
        if f5:
            f5.close()
