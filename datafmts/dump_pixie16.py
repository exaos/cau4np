#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Read data acquired by Pixie-16 VB.

Data structures:
- MCA (*.asc, *.mca): multichannel analyzer
- List mode data (*.bin)

@Vivodo
'''

from struct import unpack, calcsize
import numpy as np
import h5py


class Pixie16McaDumper:

    def __init__(self): pass

    def _get_spectrum(self, fin):
        try:
            return unpack(self._sp_fmt, fin.read(self._sp_len))
        except:
            return None

    def dump_spectra(self, fn, bins=32768, trim_zero=True):
        self._sp_fmt = "<{}i".format(bins)
        self._sp_len = calcsize(self._sp_fmt)
        specs = {}
        with open(fn, "rb") as f:
            num_spc = 0
            while True:
                spc = self._get_spectrum(f)
                if not spc:
                    break
                if not trim_zero or any(j != 0 for j in spc):
                    specs.update( { "chn_{}".format(num_spc): spc } )
                num_spc += 1
        return specs

    @classmethod
    def dump_spectra_hdf5(cls, fname, fout, bins=32768, trim_zero=True, compression="gzip"):
        f5 = h5py.File(fout, "w")
        specs = cls().dump_spectra(fname, bins=bins, trim_zero=trim_zero)
        for k,v in specs.items():
            ds = f5.create_dataset(k, (bins,), dtype="i",
                                   chunks=True, compression=compression)
            ds[:] = v
            f5.flush()
        f5.close()


class Pixie16BinDumper:

    _h_dtype = np.dtype([
            ("event_num", np.int32),
            ("channel", np.int8),
            ("slot", np.int8),
            ("crate", np.int8),
            ("header_len", np.int16),
            ("trace_len", np.int16),
            ("event_len", np.int16),
            ("event_time", np.int64),
            ("event_energy", np.int16),
            ("cfd_frac_time", np.int16),
            ("cfd_trig_src_bit", np.bool),
            ("cfd_trig_forced", np.bool),
            ("trace_out_of", np.bool),
            ("good_event", np.bool)
            ])
    _e_dtype = np.dtype([
            ("esum_trailing", np.int32),
            ("esum_leading", np.int32),
            ("esum_gap", np.int32),
            ("baseline", np.int32)
            ])

    def __init__(self): pass

    def _parse_fixed_header(self, str_h):
        """Parse the header structure into a dict."""
        _rh = unpack("<4I", str_h)
        head = np.zeros((1,), dtype=self._h_dtype)
        head["channel"] = _rh[0] & 0xF
        head["slot"] = (_rh[0] & 0xF0) >> 4
        head["crate"] = (_rh[0] & 0xF00) >> 8
        head["header_len"] = (_rh[0] & 0x1F000) >>12
        head["trace_len"] = (_rh[3] & 0x7FFF0000) >> 16
        head["event_len"] = (_rh[0] & 0x7FFE0000) >> 17
        head["event_time"] = np.int64(_rh[2] & 0xFFFF)<<32 + _rh[1]
        head["event_energy"] = (_rh[3] & 0xFFFF)
        head["cfd_frac_time"] = (_rh[2] & 0x3FFF0000) >> 16
        head["cfd_trig_src_bit"] = (_rh[2] & 0x40000000) # >> 30
        head["cfd_trig_forced"] = (_rh[2] & 0x80000000) # >> 31
        head["trace_out_of"] = (_rh[3] & 0x80000000) # >> 31
        head["good_event"] = not (_rh[0] & 0x80000000)
        return head

    def _parse_one_event(self, fin):
        """Read and parse one event from input file."""
        try:
            raw_h = fin.read(16)
            header = self._parse_fixed_header(raw_h)
            # check event block length
            assert(header["event_len"] ==
                   header["header_len"] + header["trace_len"] / 2)
            # read energy sums
            if header["header_len"] in (18, 16, 8):
                eng_sums = unpack("<4I", fin.read(16))
            else:
                eng_sums = None
            # QDC sums
            if header["header_len"] in (18, 16, 12):
                qdc_sums = unpack("<8I", fin.read(32))
            else:
                qdc_sums = None
            # external timestamp
            if header["header_len"] in (18, 10, 6):
                _raw = unpack("<2I", fin.read(8))
                ext_ts = np.int64(_raw[1] & 0xFFFF) << 32 + _raw[0]
            else:
                ext_ts = None
            # read trace
            if header["trace_len"][0] > 0:
                fmt_trace = "<{:d}h".format(header["trace_len"][0])
                _raw = unpack(fmt_trace, fin.read(calcsize(fmt_trace)))
                trace = [d & 0xFFFF for d in _raw]
            else:
                trace = None
            return (header, eng_sums, qdc_sums, ext_ts, trace)
        except:
            return None

    @classmethod
    def dump_events_to_h5_from_io(cls, fin, f5,
                                  chunks=True, shuffle=True,
                                  compression="gzip"):
        num_event = 0
        while True:
            r = cls()._parse_one_event(fin)
            if not r:
                print("Event counts:", num_event)
                break
            grp_name = "px16evt_{}".format(num_event)
            grp = f5.create_group(grp_name)
            # header
            hd = r[0]
            hd["event_num"] = num_event
            grp.create_dataset("header", dtype=cls()._h_dtype,
                               data=hd, compression=compression)
            # energy
            if r[1]:
                _d = np.zeros((1,), dtype=cls()._e_dtype)
                _d["esum_trailing"] = r[1][0]
                _d["esum_leading"] = r[1][1]
                _d["esum_gap"] = r[1][2]
                _d["baseline"] = r[1][3]
                grp.create_dataset("eng_sums", (1,), dtype=cls()._e_dtype,
                                   data=_d, compression=compression)
            # QDC sums
            if r[2]:
                grp.create_dataset("QDC_sums", (8,), dtype=np.int32,
                                   data = r[2])
            # external timestamp
            if r[3]:
                grp.create_dataset("ext_timestamp", (1,), dtype=np.int64,
                                   data = r[3])
            # trace
            if r[4]:
                grp.create_dataset("trace", (hd["trace_len"],), dtype=np.int16,
                                   data = r[4], compression=compression,
                                   chunks=chunks, shuffle=shuffle)
            f5.flush()
            # continue
            num_event += 1

    @classmethod
    def dump_events_hdf5(cls, fn, fout,
                         chunks=True, shuffle=True, compression="gzip"):
        f5 = h5py.File(fout, "w")
        with open(fn, "rb") as fin:
            cls().dump_events_to_h5_from_io(fin, f5,
                       chunks=chunks, shuffle=shuffle,
                       compression=compression)
        f5.close()


def dump_pixie16(fn, fout=None):
    if fn[-3:].lower() == "bin":
        if not fout:
            fout = fn[:-4] + "-bin.h5"
        print("Dumping event data in {} to {}".format(fn, fout))
        Pixie16BinDumper.dump_events_hdf5(fn, fout, compression=9)
    elif fn[-3:].lower() == "mca":
        if not fout:
            fout = fn[:-4] + "-mca.h5"
        print("Dumping MCA data in {} to {}".format(fn, fout))
        Pixie16McaDumper.dump_spectra_hdf5(fn, fout, compression=9)
    else:
        print("Bad filename: {}".format(fn))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(u"Usage: {} <file.[.bin|.mca]>".format(sys.argv[0]))
        sys.exit(0)

    for j in sys.argv[1:]:
        dump_pixie16(j)
