# -*- mode: yaml; coding: utf-8; -*-
meta:
  id: pixie16_set
  title: Pixie16 settings
  endian: le
seq:
  - id: mod_set
    type: pixie16_mod_set
    size: 1280 * 4
    repeat: eos
types:
  pixie16_mod_set:
    seq:
      - id: mod_num
        type: u4
      - id: mod_c_s_r_a
        type: u4
      - id: mod_c_s_r_b
        type: u4
      - id: mod_format
        type: u4
      - id: run_task
        type: u4
      - id: control_task
        type: u4
      - id: max_events
        type: u4
      - id: coinc_pattern
        type: u4
      - id: coinc_wait
        type: u4
      - id: synch_wait
        type: u4
      - id: in_synch
        type: u4
      - id: resume
        type: u4
      - id: slow_filter_range
        type: u4
      - id: fast_filter_range
        type: u4
      - id: chan_num
        type: u4
      - id: host_i_o
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: user_in
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_trig_backplane_ena
        type: u4
      - id: crate_i_d
        type: u4
      - id: slot_i_d
        type: u4
      - id: mod_i_d
        type: u4
      - id: trig_config
        type: u4
        repeat: expr
        repeat-expr: 4
      - id: u00
        type: u4
        repeat: expr
        repeat-expr: 7
      - id: host_run_time_preset
        type: f4
      - id: power_up_init_done
        type: u4
      - id: chan_c_s_ra
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: chan_c_s_rb
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: gain_d_a_c
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: offset_d_a_c
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: dig_gain
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: slow_length
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: slow_gap
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_length
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_gap
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: peak_sample
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: peak_sep
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: c_f_d_thresh
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_thresh
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: thresh_width
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: p_a_flength
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: trigger_delay
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: reset_delay
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: chan_trig_stretch
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: trace_length
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: xwait
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: trig_out_len
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: energy_low
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: log2_ebin
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: multiplicity_mask_l
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: p_s_aoffset
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: p_s_alength
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: integrator
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: b_lcut
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: baseline_percent
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: ftrigout_delay
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: log2_bweight
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: preamp_tau
        type: f4
        repeat: expr
        repeat-expr: 16
      - id: xavg
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: multiplicity_mask_h
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_trig_back_len
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: c_f_d_delay
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: c_f_d_scale
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: ext_trig_stretch
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: veto_stretch
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: extern_delay_len
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len0
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len1
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len2
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len3
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len4
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len5
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len6
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: q_d_c_len7
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: real_time_a
        type: u4
      - id: real_time_b
        type: u4
      - id: run_time_a
        type: u4
      - id: run_time_b
        type: u4
      - id: g_s_l_ttime
        type: u4
      - id: num_events_a
        type: u4
      - id: num_events_b
        type: u4
      - id: d_s_perror
        type: u4
      - id: synch_done
        type: u4
      - id: buf_head_len
        type: u4
      - id: event_head_len
        type: u4
      - id: chan_head_len
        type: u4
      - id: user_out
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: a_out_buffer
        type: u4
      - id: l_out_buffer
        type: u4
      - id: a_e_corr
        type: u4
      - id: l_e_corr
        type: u4
      - id: hardware_i_d
        type: u4
      - id: hard_variant
        type: u4
      - id: f_i_f_o_length
        type: u4
      - id: fippi_i_d
        type: u4
      - id: fippi_variant
        type: u4
      - id: d_s_prelease
        type: u4
      - id: d_s_pbuild
        type: u4
      - id: d_s_p_variant
        type: u4
      - id: u20
        type: u4
        repeat: expr
        repeat-expr: 23
      - id: live_time_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: live_time_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_peaks_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: fast_peaks_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: overflow_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: overflow_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: in_spec_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: in_spec_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: underflow_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: underflow_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: chan_events_a
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: chan_events_b
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: auto_tau
        type: u4
        repeat: expr
        repeat-expr: 16
      - id: u30
        type: u4
        repeat: expr
        repeat-expr: 177
