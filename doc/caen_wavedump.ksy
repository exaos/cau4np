# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: caen_wavedump
  title: CAEN WaveDump output
  endian: le
seq:
  - id: header
    type: caen_wavedump_header
    size: 24
  - id: wave
    type: u2
    repeat: expr
    repeat-expr: (header.rec_length-24) / 2
types:
  caen_wavedump_header:
    seq:
      - id: rec_length
        type: u4
      - id: board_id
        type: u4
      - id: pattern
        type: u4
      - id: channel
        type: u4
      - id: event_counter
        type: u4
      - id: trig_time_tag
        type: u4
