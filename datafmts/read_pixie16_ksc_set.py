# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

class Pixie16Set(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self._raw_mod_set = []
        self.mod_set = []
        i = 0
        while not self._io.is_eof():
            self._raw_mod_set.append(self._io.read_bytes((1280 * 4)))
            io = KaitaiStream(BytesIO(self._raw_mod_set[-1]))
            self.mod_set.append(self._root.Pixie16ModSet(io, self, self._root))
            i += 1


    class Pixie16ModSet(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.mod_num = self._io.read_u4le()
            self.mod_c_s_r_a = self._io.read_u4le()
            self.mod_c_s_r_b = self._io.read_u4le()
            self.mod_format = self._io.read_u4le()
            self.run_task = self._io.read_u4le()
            self.control_task = self._io.read_u4le()
            self.max_events = self._io.read_u4le()
            self.coinc_pattern = self._io.read_u4le()
            self.coinc_wait = self._io.read_u4le()
            self.synch_wait = self._io.read_u4le()
            self.in_synch = self._io.read_u4le()
            self.resume = self._io.read_u4le()
            self.slow_filter_range = self._io.read_u4le()
            self.fast_filter_range = self._io.read_u4le()
            self.chan_num = self._io.read_u4le()
            self.host_i_o = [None] * (16)
            for i in range(16):
                self.host_i_o[i] = self._io.read_u4le()

            self.user_in = [None] * (16)
            for i in range(16):
                self.user_in[i] = self._io.read_u4le()

            self.fast_trig_backplane_ena = self._io.read_u4le()
            self.crate_i_d = self._io.read_u4le()
            self.slot_i_d = self._io.read_u4le()
            self.mod_i_d = self._io.read_u4le()
            self.trig_config = [None] * (4)
            for i in range(4):
                self.trig_config[i] = self._io.read_u4le()

            self.u00 = [None] * (7)
            for i in range(7):
                self.u00[i] = self._io.read_u4le()

            self.host_run_time_preset = self._io.read_f4le()
            self.power_up_init_done = self._io.read_u4le()
            self.chan_c_s_ra = [None] * (16)
            for i in range(16):
                self.chan_c_s_ra[i] = self._io.read_u4le()

            self.chan_c_s_rb = [None] * (16)
            for i in range(16):
                self.chan_c_s_rb[i] = self._io.read_u4le()

            self.gain_d_a_c = [None] * (16)
            for i in range(16):
                self.gain_d_a_c[i] = self._io.read_u4le()

            self.offset_d_a_c = [None] * (16)
            for i in range(16):
                self.offset_d_a_c[i] = self._io.read_u4le()

            self.dig_gain = [None] * (16)
            for i in range(16):
                self.dig_gain[i] = self._io.read_u4le()

            self.slow_length = [None] * (16)
            for i in range(16):
                self.slow_length[i] = self._io.read_u4le()

            self.slow_gap = [None] * (16)
            for i in range(16):
                self.slow_gap[i] = self._io.read_u4le()

            self.fast_length = [None] * (16)
            for i in range(16):
                self.fast_length[i] = self._io.read_u4le()

            self.fast_gap = [None] * (16)
            for i in range(16):
                self.fast_gap[i] = self._io.read_u4le()

            self.peak_sample = [None] * (16)
            for i in range(16):
                self.peak_sample[i] = self._io.read_u4le()

            self.peak_sep = [None] * (16)
            for i in range(16):
                self.peak_sep[i] = self._io.read_u4le()

            self.c_f_d_thresh = [None] * (16)
            for i in range(16):
                self.c_f_d_thresh[i] = self._io.read_u4le()

            self.fast_thresh = [None] * (16)
            for i in range(16):
                self.fast_thresh[i] = self._io.read_u4le()

            self.thresh_width = [None] * (16)
            for i in range(16):
                self.thresh_width[i] = self._io.read_u4le()

            self.p_a_flength = [None] * (16)
            for i in range(16):
                self.p_a_flength[i] = self._io.read_u4le()

            self.trigger_delay = [None] * (16)
            for i in range(16):
                self.trigger_delay[i] = self._io.read_u4le()

            self.reset_delay = [None] * (16)
            for i in range(16):
                self.reset_delay[i] = self._io.read_u4le()

            self.chan_trig_stretch = [None] * (16)
            for i in range(16):
                self.chan_trig_stretch[i] = self._io.read_u4le()

            self.trace_length = [None] * (16)
            for i in range(16):
                self.trace_length[i] = self._io.read_u4le()

            self.xwait = [None] * (16)
            for i in range(16):
                self.xwait[i] = self._io.read_u4le()

            self.trig_out_len = [None] * (16)
            for i in range(16):
                self.trig_out_len[i] = self._io.read_u4le()

            self.energy_low = [None] * (16)
            for i in range(16):
                self.energy_low[i] = self._io.read_u4le()

            self.log2_ebin = [None] * (16)
            for i in range(16):
                self.log2_ebin[i] = self._io.read_u4le()

            self.multiplicity_mask_l = [None] * (16)
            for i in range(16):
                self.multiplicity_mask_l[i] = self._io.read_u4le()

            self.p_s_aoffset = [None] * (16)
            for i in range(16):
                self.p_s_aoffset[i] = self._io.read_u4le()

            self.p_s_alength = [None] * (16)
            for i in range(16):
                self.p_s_alength[i] = self._io.read_u4le()

            self.integrator = [None] * (16)
            for i in range(16):
                self.integrator[i] = self._io.read_u4le()

            self.b_lcut = [None] * (16)
            for i in range(16):
                self.b_lcut[i] = self._io.read_u4le()

            self.baseline_percent = [None] * (16)
            for i in range(16):
                self.baseline_percent[i] = self._io.read_u4le()

            self.ftrigout_delay = [None] * (16)
            for i in range(16):
                self.ftrigout_delay[i] = self._io.read_u4le()

            self.log2_bweight = [None] * (16)
            for i in range(16):
                self.log2_bweight[i] = self._io.read_u4le()

            self.preamp_tau = [None] * (16)
            for i in range(16):
                self.preamp_tau[i] = self._io.read_f4le()

            self.xavg = [None] * (16)
            for i in range(16):
                self.xavg[i] = self._io.read_u4le()

            self.multiplicity_mask_h = [None] * (16)
            for i in range(16):
                self.multiplicity_mask_h[i] = self._io.read_u4le()

            self.fast_trig_back_len = [None] * (16)
            for i in range(16):
                self.fast_trig_back_len[i] = self._io.read_u4le()

            self.c_f_d_delay = [None] * (16)
            for i in range(16):
                self.c_f_d_delay[i] = self._io.read_u4le()

            self.c_f_d_scale = [None] * (16)
            for i in range(16):
                self.c_f_d_scale[i] = self._io.read_u4le()

            self.ext_trig_stretch = [None] * (16)
            for i in range(16):
                self.ext_trig_stretch[i] = self._io.read_u4le()

            self.veto_stretch = [None] * (16)
            for i in range(16):
                self.veto_stretch[i] = self._io.read_u4le()

            self.extern_delay_len = [None] * (16)
            for i in range(16):
                self.extern_delay_len[i] = self._io.read_u4le()

            self.q_d_c_len0 = [None] * (16)
            for i in range(16):
                self.q_d_c_len0[i] = self._io.read_u4le()

            self.q_d_c_len1 = [None] * (16)
            for i in range(16):
                self.q_d_c_len1[i] = self._io.read_u4le()

            self.q_d_c_len2 = [None] * (16)
            for i in range(16):
                self.q_d_c_len2[i] = self._io.read_u4le()

            self.q_d_c_len3 = [None] * (16)
            for i in range(16):
                self.q_d_c_len3[i] = self._io.read_u4le()

            self.q_d_c_len4 = [None] * (16)
            for i in range(16):
                self.q_d_c_len4[i] = self._io.read_u4le()

            self.q_d_c_len5 = [None] * (16)
            for i in range(16):
                self.q_d_c_len5[i] = self._io.read_u4le()

            self.q_d_c_len6 = [None] * (16)
            for i in range(16):
                self.q_d_c_len6[i] = self._io.read_u4le()

            self.q_d_c_len7 = [None] * (16)
            for i in range(16):
                self.q_d_c_len7[i] = self._io.read_u4le()

            self.real_time_a = self._io.read_u4le()
            self.real_time_b = self._io.read_u4le()
            self.run_time_a = self._io.read_u4le()
            self.run_time_b = self._io.read_u4le()
            self.g_s_l_ttime = self._io.read_u4le()
            self.num_events_a = self._io.read_u4le()
            self.num_events_b = self._io.read_u4le()
            self.d_s_perror = self._io.read_u4le()
            self.synch_done = self._io.read_u4le()
            self.buf_head_len = self._io.read_u4le()
            self.event_head_len = self._io.read_u4le()
            self.chan_head_len = self._io.read_u4le()
            self.user_out = [None] * (16)
            for i in range(16):
                self.user_out[i] = self._io.read_u4le()

            self.a_out_buffer = self._io.read_u4le()
            self.l_out_buffer = self._io.read_u4le()
            self.a_e_corr = self._io.read_u4le()
            self.l_e_corr = self._io.read_u4le()
            self.hardware_i_d = self._io.read_u4le()
            self.hard_variant = self._io.read_u4le()
            self.f_i_f_o_length = self._io.read_u4le()
            self.fippi_i_d = self._io.read_u4le()
            self.fippi_variant = self._io.read_u4le()
            self.d_s_prelease = self._io.read_u4le()
            self.d_s_pbuild = self._io.read_u4le()
            self.d_s_p_variant = self._io.read_u4le()
            self.u20 = [None] * (23)
            for i in range(23):
                self.u20[i] = self._io.read_u4le()

            self.live_time_a = [None] * (16)
            for i in range(16):
                self.live_time_a[i] = self._io.read_u4le()

            self.live_time_b = [None] * (16)
            for i in range(16):
                self.live_time_b[i] = self._io.read_u4le()

            self.fast_peaks_a = [None] * (16)
            for i in range(16):
                self.fast_peaks_a[i] = self._io.read_u4le()

            self.fast_peaks_b = [None] * (16)
            for i in range(16):
                self.fast_peaks_b[i] = self._io.read_u4le()

            self.overflow_a = [None] * (16)
            for i in range(16):
                self.overflow_a[i] = self._io.read_u4le()

            self.overflow_b = [None] * (16)
            for i in range(16):
                self.overflow_b[i] = self._io.read_u4le()

            self.in_spec_a = [None] * (16)
            for i in range(16):
                self.in_spec_a[i] = self._io.read_u4le()

            self.in_spec_b = [None] * (16)
            for i in range(16):
                self.in_spec_b[i] = self._io.read_u4le()

            self.underflow_a = [None] * (16)
            for i in range(16):
                self.underflow_a[i] = self._io.read_u4le()

            self.underflow_b = [None] * (16)
            for i in range(16):
                self.underflow_b[i] = self._io.read_u4le()

            self.chan_events_a = [None] * (16)
            for i in range(16):
                self.chan_events_a[i] = self._io.read_u4le()

            self.chan_events_b = [None] * (16)
            for i in range(16):
                self.chan_events_b[i] = self._io.read_u4le()

            self.auto_tau = [None] * (16)
            for i in range(16):
                self.auto_tau[i] = self._io.read_u4le()

            self.u30 = [None] * (177)
            for i in range(177):
                self.u30[i] = self._io.read_u4le()




