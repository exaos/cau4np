
# `spectrafmt`: Python utility to read spectra in various formats

Due to different data-acquisition systems, we may deposite many spectra in various formats in nuclear physics experiments. This bundle of python scripts is used to read various spectra into python for further processing by using many tools in the python ecosystem, e.g., numpy, scipy, matplotlib, etc.

## Formats currently supported

- `read_mca.py` :: To handle `.mca` files acquired by MCA8000A using software *PMCA.exe* from AMPTEK.
- `read_ortec.py` :: To handle various files acquired by softwares from ORTEC. This script currently supports `.chn` (Integer Data File) and `.spc` (Raw or Net Spectrum File in Real/Integer format).

## Changelog

- 2017-11-14
  - Support `.mca`, `.chn`, `.spc`.
  - Make codes compatible with python2 and python3.


