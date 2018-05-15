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
    size: (event_block.blk_count * event_block.event_size) * 4 + 8
    repeat: expr
    repeat-expr: eos
  - id: footer
    contents: [0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF, 0xFFFF]
types:
  kmax_header:
    seq:
      - id: magic
        contents: [ 0x02, 0x00, 0x00, 0x01 ]
  kmax_event_block:
    seq:
      - id: event_size
        type: u2
      - id: event_type
        type: u2
      - id: blk_count
        type: u4
      - id: event_entry
        type: u4
        repeat: expr
        repeat-expr: event_size
