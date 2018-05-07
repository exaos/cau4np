# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: ortec_spc
  title: ORTEC Real Format Spectrum Files (partial)
  endian: le
seq:
  - id: header
    type: ortec_spc_real_header
    size: 128
  - id: acq_info
    type: ortec_acq_record
    size: 128
  - id: sample_desc
    type: ortec_sample_desc_record
    size: 128 #??
  - id: detector_desc
    type: ortec_detector_desc_record
    size: 128 #??
  - id: analysis_parameters
    type: ortec_analysis_par_record
    size: 128 #??
  - id: absorption_correction_desc
    type: ortec_absorption_cor_desc_record
    size: 128
  - id: absorption_corr_data
    type: ortec_absorption_cor_data_record
    size: 128
  - id: geom_corr_desc
    type: ortec_geom_correction_desc_record
    size: 128
  - id: geom_corr_data
    type: ortec_geom_correction_data_record
    size: 128
  - id: calibration
    type: ortec_cali_record
    size: 128 * 3 #??
  - id: roi
    type: ortec_roi_record
    size: 128 * 3 #???
  - id: hw_par
    type: ortec_hw_par_record
    size: 128 * 4
  - id: personality
    type: ortec_personality_record
    size: 128
  - id: table_desc
    type: ortec_table_desc_record
    size: 128
  - id: table_data
    type: ortec_table_data_record
    size: 128
  - id: spc
    type: f4
    repeat: expr
    repeat-expr: number_of_channels
types:
  ortec_spc_real_header:
  ortec_acq_record:
  ortec_sample_desc_record:
  ortec_detector_desc_record:
  ortec_analysis_par_record:
  ortec_absorption_cor_desc_record:
