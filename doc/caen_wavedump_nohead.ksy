# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: caen_wavedump
  title: CAEN WaveDump output without header
  endian: le
seq:
  - id: channel
    type: u2
  - id: wave
    type: u2
    repeat: expr
    repeat-expr: _
