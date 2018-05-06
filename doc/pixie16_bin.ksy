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
      - id: header
        type: pixie_header
        size: 16
      - id: trace
        type: u4
        repeat: expr
        repeat-expr: trace_len
    instances:
      channel:
        value: header.r0 & 0xF
      slot:
        value: (header.r0 & 0xF0) >> 4
      crate:
        value: (header.r0 & 0xF00) >> 8
      header_len:
        value: (header.r0 & 0x1_F000) >> 12
      event_len:
        value: (header.r0 & 0x7FFE_0000) >> 17
      finish_code:
        value: (header.r0 & 0x8000_0000) >> 31
      event_time:
        value: (header.r2 & 0xFFFF) + header.r1
      event_energy:
        value: header.r3 & 0xFFFF
      trace_len:
        value: (header.r3 &0x7FFF_0000) >> 16
  pixie_header:
    seq:
      - id: r0
        type: u4
      - id: r1
        type: u4
      - id: r2
        type: u4
      - id: r3
        type: u4
