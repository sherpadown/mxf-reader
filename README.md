# MXF-Reader

mxf-reader analyzes, extracts or decrypts data from complete or broken MXF.


## Usage


### Installation 

```
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

#### Using

```
$ python -m mxf_reader -h
usage: mxf_reader [-h] [-f FILENAME] [-x EXTRACT] [-k KEY] [-v] [-n] [--filter FILTER] [--fuzzy] [--limit LIMIT] [--slow]

options:
  -h, --help							show this help message and exit
  -f FILENAME, --filename FILENAME		<mxf> = mxf filename
  -x EXTRACT, --extract EXTRACT			<directory> = extract each KLV into files
  -k KEY, --key KEY						AES Key, ex. --key 00000000000000000000000000000000
  -v, --verbose							increase output verbosity
  -n, --no-resolv						Do not resolv UL (speed)
  --filter FILTER						filter by name
  --fuzzy								Fuzzy mode only (very slow)
  --limit LIMIT							stop after x klv parsed
  --slow								Slowdown parse to avoid flood loadavg
```

You can use mxf-reader with this parameters :

```
$ python -m mxf_reader -f tests/assets/2D.mxf
      offset │ uuid                                │ ber      	:	 data-size │                             data │ name
           0 │ 060e2b34.02050101.0d010201.01020400 │ 83.000078	:	       120 │ 00010002000000010000000000000000 │ Partition Pack - Header - Closed & Complete
         140 │ 060e2b34.02050101.0d010201.01050100 │ 83.000596	:	      1430 │ 0000004f000000120201060e2b340101 │ Primer Pack
        1590 │ 060e2b34.02530101.0d010101.01012f00 │ 83.0000be	:	       190 │ 3c0a0010aaffbd07420e44a2b3f87d3c │ Preface
        1800 │ 060e2b34.02530101.0d010101.01013000 │ 83.0000d8	:	       216 │ 3c0a0010c00c5d91bc1b4e58aefabf33 │ Identification
        2036 │ 060e2b34.02530101.0d010101.01011800 │ 83.00005c	:	        92 │ 3c0a0010acc6d12cda0c465b861a1c33 │ Content Storage
        2148 │ 060e2b34.02530101.0d010101.01012300 │ 83.000048	:	        72 │ 3c0a0010bf8a6ebc3aca4164a47e45e0 │ Essence Container Data
        2240 │ 060e2b34.02530101.0d010101.01013600 │ 83.0000a0	:	       160 │ 3c0a001096b13153bd5d4cd29abcd608 │ Material Package
        2420 │ 060e2b34.02530101.0d010101.01013b00 │ 83.000070	:	       112 │ 3c0a0010005ea82d6afb4a37aae4d74b │ Timeline Track
        2552 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a00108afb9187a608464f85713462 │ Sequence
        2652 │ 060e2b34.02530101.0d010101.01011400 │ 83.00004b	:	        75 │ 3c0a00108fe911af95d4464e9e794651 │ Timecode Component
        2747 │ 060e2b34.02530101.0d010101.01013b00 │ 83.00006e	:	       110 │ 3c0a0010f8427198af884d4f8c9855f3 │ Timeline Track
        2877 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a0010e2bfd055e5d249a0bfcb4da8 │ Sequence
        2977 │ 060e2b34.02530101.0d010101.01011100 │ 83.00006c	:	       108 │ 3c0a00106daf21bab69a41c99ec54f4f │ Source Clip
        3105 │ 060e2b34.02530101.0d010101.01013700 │ 83.000116	:	       278 │ 3c0a0010b87f0871f98446d39a842893 │ Source Package
        3403 │ 060e2b34.02530101.0d010101.01013b00 │ 83.000070	:	       112 │ 3c0a00106378d2218be746d28508fedf │ Timeline Track
        3535 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a001075ef53606937484a9ee14472 │ Sequence
        3635 │ 060e2b34.02530101.0d010101.01011400 │ 83.00004b	:	        75 │ 3c0a001059cf1ad86f314b5db0164871 │ Timecode Component
        3730 │ 060e2b34.02530101.0d010101.01013b00 │ 83.00006e	:	       110 │ 3c0a0010d4e733700afb45329cc796c6 │ Timeline Track
        3860 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a0010e2f035aa64684a7f98eddfa7 │ Sequence
        3960 │ 060e2b34.02530101.0d010101.01011100 │ 83.00006c	:	       108 │ 3c0a0010c93d2257b09a4dbea24c782e │ Source Clip
        4088 │ 060e2b34.02530101.0d010101.01012900 │ 83.0000bd	:	       189 │ 3c0a00102cb46505be6b41c3abbe8848 │ RGBA Essence Descriptor
        4297 │ 060e2b34.02530101.0d010101.01015a00 │ 83.0000b5	:	       181 │ 3c0a00106054268f8fdf47ba98db7167 │ JPEG2000 Picture Sub-Descriptor
        4498 │ 060e2b34.01010102.03010210.01000000 │ 83.002e5a	:	     11866 │ 00000000000000000000000000000000 │ KLV Fill item (SMPTE)
       16384 │ 060e2b34.02050101.0d010201.01030400 │ 83.000078	:	       120 │ 00010002000000010000000000004000 │ Partition Pack - Body - Closed & Complete
       16524 │ 060e2b34.01020101.0d010301.15010801 │ 83.009cc8	:	     40136 │ ff4fff51002f00040000100000000870 │ Picture Essence - 1 frame
       56680 │ 060e2b34.02050101.0d010201.01040400 │ 83.000078	:	       120 │ 0001000200000001000000000000dd68 │ Partition Pack - Footer - Closed & Complete
       56820 │ 060e2b34.02530101.0d010201.01100100 │ 83.000083	:	       131 │ 3c0a00101c86aa0136fb414ebcd47120 │ Index Table Segment (2-bytes LocalTags, 2-bytes Length)
```

Likewise, you can use with piped / streamed (prototype) content :

```
$ cat tests/assets/2D.mxf | python -m mxf_reader -f -
      offset │ uuid                                │ ber      	:	 data-size │                             data │ name
           0 │ 060e2b34.02050101.0d010201.01020400 │ 83.000078	:	       120 │ 00010002000000010000000000000000 │ Partition Pack - Header - Closed & Complete
         140 │ 060e2b34.02050101.0d010201.01050100 │ 83.000596	:	      1430 │ 0000004f000000120201060e2b340101 │ Primer Pack
        1590 │ 060e2b34.02530101.0d010101.01012f00 │ 83.0000be	:	       190 │ 3c0a0010aaffbd07420e44a2b3f87d3c │ Preface
        1800 │ 060e2b34.02530101.0d010101.01013000 │ 83.0000d8	:	       216 │ 3c0a0010c00c5d91bc1b4e58aefabf33 │ Identification
        2036 │ 060e2b34.02530101.0d010101.01011800 │ 83.00005c	:	        92 │ 3c0a0010acc6d12cda0c465b861a1c33 │ Content Storage
		(...)
```
