# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Pixie16Bin(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.event = []
        i = 0
        while not self._io.is_eof():
            self.event.append(self._root.EventType(self._io, self, self._root))
            i += 1


    class PixieQdcSums(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.qdc_sums = [None] * (8)
            for i in range(8):
                self.qdc_sums[i] = self._io.read_u4le()



    class PixieExtClockTimestamp(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ext_ts_lo = self._io.read_u4le()
            self.ext_ts_hi = self._io.read_u4le()


    class PixieFixedHeader(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r0 = self._io.read_u4le()
            self.r1 = self._io.read_u4le()
            self.r2 = self._io.read_u4le()
            self.r3 = self._io.read_u4le()


    class EventType(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw_fixed_h = self._io.read_bytes(16)
            io = KaitaiStream(BytesIO(self._raw_fixed_h))
            self.fixed_h = self._root.PixieFixedHeader(io, self, self._root)
            if  ((self.header_len == 8) or (self.header_len == 16) or (self.header_len == 18)) :
                self._raw_eng_sums = self._io.read_bytes(16)
                io = KaitaiStream(BytesIO(self._raw_eng_sums))
                self.eng_sums = self._root.PixieRawEngSums(io, self, self._root)

            if  ((self.header_len == 12) or (self.header_len == 16) or (self.header_len == 18)) :
                self._raw_qdc_sums = self._io.read_bytes(32)
                io = KaitaiStream(BytesIO(self._raw_qdc_sums))
                self.qdc_sums = self._root.PixieQdcSums(io, self, self._root)

            if  ((self.header_len == 6) or (self.header_len == 10) or (self.header_len == 18)) :
                self._raw_ext_clock_timestamp = self._io.read_bytes(8)
                io = KaitaiStream(BytesIO(self._raw_ext_clock_timestamp))
                self.ext_clock_timestamp = self._root.PixieExtClockTimestamp(io, self, self._root)

            if self.trace_len > 0:
                self.trace = [None] * (self.trace_len)
                for i in range(self.trace_len):
                    self.trace[i] = self._io.read_u2le()



        @property
        def cfd_frac_time(self):
            if hasattr(self, '_m_cfd_frac_time'):
                return self._m_cfd_frac_time if hasattr(self, '_m_cfd_frac_time') else None

            self._m_cfd_frac_time = ((self.fixed_h.r2 & 1073676288) >> 16)
            return self._m_cfd_frac_time if hasattr(self, '_m_cfd_frac_time') else None

        @property
        def event_len(self):
            if hasattr(self, '_m_event_len'):
                return self._m_event_len if hasattr(self, '_m_event_len') else None

            self._m_event_len = ((self.fixed_h.r0 & 2147352576) >> 17)
            return self._m_event_len if hasattr(self, '_m_event_len') else None

        @property
        def cfd_trig_forced(self):
            if hasattr(self, '_m_cfd_trig_forced'):
                return self._m_cfd_trig_forced if hasattr(self, '_m_cfd_trig_forced') else None

            self._m_cfd_trig_forced = ((self.fixed_h.r2 & 2147483648) >> 31)
            return self._m_cfd_trig_forced if hasattr(self, '_m_cfd_trig_forced') else None

        @property
        def event_time_hi(self):
            if hasattr(self, '_m_event_time_hi'):
                return self._m_event_time_hi if hasattr(self, '_m_event_time_hi') else None

            self._m_event_time_hi = (self.fixed_h.r2 & 65535)
            return self._m_event_time_hi if hasattr(self, '_m_event_time_hi') else None

        @property
        def trace_out_of_range(self):
            if hasattr(self, '_m_trace_out_of_range'):
                return self._m_trace_out_of_range if hasattr(self, '_m_trace_out_of_range') else None

            self._m_trace_out_of_range = ((self.fixed_h.r3 & 2147483648) >> 31)
            return self._m_trace_out_of_range if hasattr(self, '_m_trace_out_of_range') else None

        @property
        def slot(self):
            if hasattr(self, '_m_slot'):
                return self._m_slot if hasattr(self, '_m_slot') else None

            self._m_slot = ((self.fixed_h.r0 & 240) >> 4)
            return self._m_slot if hasattr(self, '_m_slot') else None

        @property
        def crate(self):
            if hasattr(self, '_m_crate'):
                return self._m_crate if hasattr(self, '_m_crate') else None

            self._m_crate = ((self.fixed_h.r0 & 3840) >> 8)
            return self._m_crate if hasattr(self, '_m_crate') else None

        @property
        def cfd_trig_src_bit(self):
            if hasattr(self, '_m_cfd_trig_src_bit'):
                return self._m_cfd_trig_src_bit if hasattr(self, '_m_cfd_trig_src_bit') else None

            self._m_cfd_trig_src_bit = ((self.fixed_h.r2 & 1073741824) >> 30)
            return self._m_cfd_trig_src_bit if hasattr(self, '_m_cfd_trig_src_bit') else None

        @property
        def header_len(self):
            if hasattr(self, '_m_header_len'):
                return self._m_header_len if hasattr(self, '_m_header_len') else None

            self._m_header_len = ((self.fixed_h.r0 & 126976) >> 12)
            return self._m_header_len if hasattr(self, '_m_header_len') else None

        @property
        def event_time_lo(self):
            if hasattr(self, '_m_event_time_lo'):
                return self._m_event_time_lo if hasattr(self, '_m_event_time_lo') else None

            self._m_event_time_lo = self.fixed_h.r1
            return self._m_event_time_lo if hasattr(self, '_m_event_time_lo') else None

        @property
        def trace_len(self):
            if hasattr(self, '_m_trace_len'):
                return self._m_trace_len if hasattr(self, '_m_trace_len') else None

            self._m_trace_len = ((self.fixed_h.r3 & 2147418112) >> 16)
            return self._m_trace_len if hasattr(self, '_m_trace_len') else None

        @property
        def channel(self):
            if hasattr(self, '_m_channel'):
                return self._m_channel if hasattr(self, '_m_channel') else None

            self._m_channel = (self.fixed_h.r0 & 15)
            return self._m_channel if hasattr(self, '_m_channel') else None

        @property
        def event_energy(self):
            if hasattr(self, '_m_event_energy'):
                return self._m_event_energy if hasattr(self, '_m_event_energy') else None

            self._m_event_energy = (self.fixed_h.r3 & 65535)
            return self._m_event_energy if hasattr(self, '_m_event_energy') else None

        @property
        def finish_code(self):
            if hasattr(self, '_m_finish_code'):
                return self._m_finish_code if hasattr(self, '_m_finish_code') else None

            self._m_finish_code = ((self.fixed_h.r0 & 2147483648) >> 31)
            return self._m_finish_code if hasattr(self, '_m_finish_code') else None


    class PixieRawEngSums(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.eng_sum_trailing = self._io.read_u4le()
            self.eng_sum_leading = self._io.read_u4le()
            self.eng_sum_gap = self._io.read_u4le()
            self.baseline = self._io.read_u4le()



