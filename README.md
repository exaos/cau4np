# `cau4np` -- Collections of analysis utilities for nuclear physics

Due to different data-acquisition systems, we may deposite vast spectra in various formats in nuclear physics experiments. This bundle of python scripts is used to read spectra in various formats into python for further processing by using tools in the python ecosystem, e.g., numpy, scipy, matplotlib, etc.

## Formats currently supported

- `datafmts/read_pmca.py` :: To handle `.mca` files acquired by MCA8000A using software *PMCA.exe* from AMPTEK.
- `datafmts/read_ortec.py` :: To handle various data acquired by softwares from ORTEC. This script currently supports `.chn` (Integer Data File) and `.spc` (Raw or Net Spectrum File in Real/Integer format).

## Changelog

- 2017-11-27
  - Define standards for representation of spectra in `doc/sample-*.yaml`.
  - Now, `datafmts/read_ortec.py` is not comptable with python2.
- 2017-11-14
  - Support `.mca`, `.chn`, `.spc`.
  - Make codes compatible with python2 and python3.
