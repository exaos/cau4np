# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: ortec_chn
  title: ORTEC Integer Data Files
  endian: le
seq:
  - id: header_block
    type: chn_header
    size: 32
  - id: spec
    type: u4
    repeat: expr
    repeat-expr: header_block.num_of_chns
  - id: info_block
    type: spec_info
    size: 512
types:
  chn_header:
    doc-ref: ORTEC File Structures, sec 3.1, pp.5
    seq:
      - id: magic
        contents: [0xFF, 0xFF]
      - id: num_mca
        type: s2
      - id: num_segment
        type: s2
      - id: start_time_seconds
        type: str
        size: 2
        encoding: ASCII
      - id: real_time
        type: s4
      - id: live_time
        type: s4
      - id: start_date
        type: str
        size: 8
        encoding: ASCII
      - id: start_time
        type: str
        size: 4
        encoding: ASCII
      - id: channel_offset
        type: u2
      - id: num_of_chns
        type: s2
  spec_info:
    seq:
      - id: magic
        type: s2
    types:
      eng_cali_info:
        seq:
          - id: eng_cali_zero_intercept
            type: f4
          - id: eng_cali_slope
            type: f4
          - id: eng_cali_quadratic
            type: f4
            if: _parent.magic == -102
      shape_cali_info:
        seq:
          - id: peak_shape_cali_zero_intercept
            type: f4
          - id: peak_shape_cali_slope
            type: f4
          - id: peak_shape_cali_quadratic
            type: f4
            if: _parent.magic == -102
      description_info:
        seq:
          - id: len_of_description
            type: s1
          - id: description
            type: strz
            encoding: ASCII
            size: 63
      spec_info_old_alpha:
        seq:
          - id: sample_type_name
            type: strz
            size: 32
            encoding: ASCII
          - id: collection_date
            type: strz
            size: 10
            encoding: ASCII
          - id: collection_time
            type: strz
            size: 10
            encoding: ASCII
          - id: sample_total_volume
            type: f4
          - id: sample_aliquot_volume
            type: f4
          - id: tracer_amount
            type: f4
          - id: volume_units
            type: str
            size: 2
            encoding: ASCII
          - id: det_efficiency
            type: f4
          - id: old_cali_intercept
            type: f4
          - id: old_cali_slope
            type: f4
          - id: old_cali_shape
            type: f4
          - id: old_cali_efficiency
            type: f4
          - id: old_bkg_counts
            type: s4
          - id: old_bkg_cpm
            type: s4
          - id: group_name
            type: strz
            size: 30
            encoding: ASCII
    instances:
      eng_cali:
        pos: 4
        type: eng_cali_info
      shape_cali:
        pos: 16
        type: shape_cali_info
      detector_description:
        type: description_info
        pos: 256
      sample_description:
        type: description_info
        pos: 320
      magic_old_alpha:
        pos: 384
        type: u4
      old_alpha_info:
        type: spec_info_old_alpha
        pos: 388
        size: 124
        if: is_old_alpha
      is_old_alpha:
        value: (magic == -102) and (magic_old_alpha == 0x53495641)
