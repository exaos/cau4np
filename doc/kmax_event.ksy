# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: kmax_event
  title: Kmax Event Output
  endian: be
seq:
  - id: header
    type: kmax_header
    size: 512
  - id: event_block
    type: kmax_event_block
    repeat: until
    repeat-until: _.is_footer
  - id: event_footer
    contents: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
types:
  kmax_header:
    seq:
      - id: magic
        contents: [ 0x02, 0x00, 0x00, 0x01 ]
  kmax_event_block:
    seq:
      - id: event_par
        type: u4
      - id: blk_count
        type: u4
      - id: event_entry
        type: kmax_event_entry
        repeat: expr
        repeat-expr: blk_count
    types:
      kmax_event_entry:
        seq:
          - id: par
            type: u4
            repeat: expr
            repeat-expr: _parent.event_size
    instances:
      is_footer:
        value: event_par == 0xFFFF_FFFF and blk_count == 0xFFFF_FFFF
      event_size:
        value: (event_par & 0xFFFF)
      event_type:
        value: (event_par & 0xFFFF_0000) >> 16
