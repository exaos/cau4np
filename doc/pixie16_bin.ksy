# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: pixie16_bin
  title: PIXIE16 List-mode Output
  endian: le
seq:
  - id: event
    type: event_type
    repeat: eos
types:
  event_type:
    seq:
      - id: fixed_h
        type: pixie_fixed_header
        size: 16
      - id: eng_sums
        type: pixie_raw_eng_sums
        size: 16
        if: (header_len == 8) or (header_len == 16) or (header_len == 18)
      - id: qdc_sums
        type: pixie_qdc_sums
        size: 32
        if: (header_len == 12) or (header_len == 16) or (header_len == 18)
      - id: ext_clock_timestamp
        type: pixie_ext_clock_timestamp
        size: 8
        if: (header_len == 6) or (header_len == 10) or (header_len == 18)
      - id: trace
        type: u2
        repeat: expr
        repeat-expr: trace_len
        if: trace_len > 0
    instances:
      channel:
        value: fixed_h.r0 & 0xF
      slot:
        value: (fixed_h.r0 & 0xF0) >> 4
      crate:
        value: (fixed_h.r0 & 0xF00) >> 8
      header_len:
        value: (fixed_h.r0 & 0x1_F000) >> 12
      event_len:
        value: (fixed_h.r0 & 0x7FFE_0000) >> 17
      finish_code:
        value: (fixed_h.r0 & 0x8000_0000) >> 31
      event_time_lo:
        value: fixed_h.r1
      event_time_hi:
        value: fixed_h.r2 & 0xFFFF
      cfd_frac_time:
        value: (fixed_h.r2 & 0x3FFF_0000) >> 16
      cfd_trig_src_bit:
        value: (fixed_h.r2 & 0x4000_0000) >> 30
      cfd_trig_forced:
        value: (fixed_h.r2 & 0x8000_0000) >> 31
      event_energy:
        value: fixed_h.r3 & 0xFFFF
      trace_len:
        value: (fixed_h.r3 & 0x7FFF_0000) >> 16
      trace_out_of_range:
        value: (fixed_h.r3 & 0x8000_0000) >> 31
  pixie_fixed_header:
    seq:
      - id: r0
        type: u4
      - id: r1
        type: u4
      - id: r2
        type: u4
      - id: r3
        type: u4
  pixie_raw_eng_sums:
    seq:
      - id: eng_sum_trailing
        type: u4
      - id: eng_sum_leading
        type: u4
      - id: eng_sum_gap
        type: u4
      - id: baseline
        type: u4
  pixie_qdc_sums:
    seq:
      - id: qdc_sums
        type: u4
        repeat: expr
        repeat-expr: 8
  pixie_ext_clock_timestamp:
    seq:
      - id: ext_ts_lo
        type: u4
      - id: ext_ts_hi
        type: u4
