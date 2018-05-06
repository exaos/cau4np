# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: pixie16_mca
  endian: le
seq:
  - id: ch_spec
    type: spec_array
    repeat: eos
types:
  spec_array:
    seq:
      - id: bin_content
        type: s4
        repeat: expr
        repeat-expr: 32768
