# MXF-Reader

mxf-reader analyzes, extracts or decrypts data from complete or broken MXF.


## Usage


### Installation 

```
$ uv venv
$ source .venv/bin/activate
$ uv sync
```

### Using

```
$ python -m mxf_reader -h
usage: mxf_reader [-h] [-f FILENAME] [-x EXTRACT] [-k KEY] [-v] [-n] [--filter FILTER] [--fuzzy] [--limit LIMIT] [--slow]

options:
  -h, --help                            show this help message and exit
  -f FILENAME, --filename FILENAME      <mxf> = mxf filename
  -x EXTRACT, --extract EXTRACT         <directory> = extract each KLV into files
  -k KEY, --key KEY                     AES Key, ex. --key 00000000000000000000000000000000
  -v, --verbose                         increase output verbosity
  -n, --no-resolv                       Do not resolv UL (speed)
  --filter FILTER                       filter by name
  --fuzzy                               Fuzzy mode only (very slow)
  --limit LIMIT                         stop after x klv parsed
  --slow                                Slowdown parse to avoid flood loadavg
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


### Use with Docker

```
$ make docker.build         # build docker
$ make docker.run.tests     # run tests
```

or 

```
$ docker run -v "/local/path/assets:/assets" -it --rm mxf-reader:latest -f /assets/your.mxf
```




## Examples


### Read MXF with verbose

```
$ python -m mxf_reader -f tests/assets/2D.mxf -vvv
```

Output : 

```
Filename tests/assets/2D.mxf (57031 bytes)
610 SMPTE Universal Labels loaded
162 SMPTE Local Tags loaded
  offset │ uuid                                │ ber      	:	 data-size │                             data │ name
	   0 │ 060e2b34.02050101.0d010201.01020400 │ 83.000078	:	       120 │ 00010002000000010000000000000000 │ Partition Pack - Header - Closed & Complete
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Major Version                                       ║  1
 ║   Minor Version                                       ║  2
 ║   KAGSize                                             ║  1
 ║   ThisPartition                                       ║  0
 ║   PreviousPartition                                   ║  0
 ║   FooterPartition                                     ║  56680
 ║   HeaderByteCount                                     ║  16244
 ║   IndexByteCount                                      ║  0
 ║   IndexSID                                            ║  0
 ║   BodyOffset                                          ║  0
 ║   BodySID                                             ║  0
 ║   Operational Pattern                                 ║  060e2b34.04010102.0d010201.10000000	(Operational Pattern - Specialized Pattern - OP Atom - SMPTE)
 ║   EssenceContainers                                   ║  2 item(s): 060e2b34.04010103.0d010301.027f0100, 060e2b34.04010107.0d010301.020c0100
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 41-44-46
 ║   Parser                                              ║  partition_pack
 ║   Data - Key                                          ║  060e2b34020501010d01020101020400
 ║   Data - Length                                       ║  000078 (120 bytes)
 ║   Data - Value [0]                                    ║  000100020000000100000000000000000000000000000000000000000000dd68000000000000
 ║   Data - Value [1]                                    ║  3f74000000000000000000000000000000000000000000000000060e2b34040101020d010201
 ║   Data - Value [2]                                    ║  100000000000000200000010060e2b34040101030d010301027f0100060e2b34040101070d01
 ║   Data - Value [3]                                    ║  0301020c0100
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	 140 │ 060e2b34.02050101.0d010201.01050100 │ 83.000596	:	      1430 │ 0000004f000000120201060e2b340101 │ Primer Pack
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   0201                                                ║  060e2b34.01010102.04070100.00000000 - Statically Local Tags - Data Definition
 ║   0202                                                ║  060e2b34.01010102.07020201.01030000 - Statically Local Tags - Duration
 ║   1001                                                ║  060e2b34.01010102.06010104.06090000 - Statically Local Tags - Structural Components UID
 ║   1101                                                ║  060e2b34.01010102.06010103.01000000 - Statically Local Tags - SourcePackageID
 ║   1102                                                ║  060e2b34.01010102.06010103.02000000 - Statically Local Tags - SourceTrackID
 ║   1201                                                ║  060e2b34.01010102.07020103.01040000 - Statically Local Tags - Start Position
 ║   1501                                                ║  060e2b34.01010102.07020103.01050000 - Statically Local Tags - Start Timecode
 ║   1502                                                ║  060e2b34.01010102.04040101.02060000 - Statically Local Tags - Rounded Timecode Base
 ║   1503                                                ║  060e2b34.01010101.04040101.05000000 - Statically Local Tags - Drop Frame
 ║   1901                                                ║  060e2b34.01010102.06010104.05010000 - Statically Local Tags - Packages
 ║   1902                                                ║  060e2b34.01010102.06010104.05020000 - Statically Local Tags - Essence Container Data
 ║   2701                                                ║  060e2b34.01010102.06010106.01000000 - Statically Local Tags - Linked Package UID
 ║   3001                                                ║  060e2b34.01010101.04060101.00000000 - Statically Local Tags - Sample Rate
 ║   3002                                                ║  060e2b34.01010101.04060102.00000000 - Statically Local Tags - Container Duration
 ║   3004                                                ║  060e2b34.01010102.06010104.01020000 - Statically Local Tags - Essence Container
 ║   3006                                                ║  060e2b34.01010105.06010103.05000000 - Statically Local Tags - Linked Track ID
 ║   3201                                                ║  060e2b34.01010102.04010601.00000000 - Statically Local Tags - Picture Essence Coding
 ║   3202                                                ║  060e2b34.01010101.04010502.01000000 - Statically Local Tags - Stored Height
 ║   3203                                                ║  060e2b34.01010101.04010502.02000000 - Statically Local Tags - Stored Width
 ║   320C                                                ║  060e2b34.01010101.04010301.04000000 - Statically Local Tags - Frame Layout
 ║   320E                                                ║  060e2b34.01010101.04010101.01000000 - Statically Local Tags - Aspect Ratio
 ║   3401                                                ║  060e2b34.01010102.04010503.06000000 - Statically Local Tags - PixelLayout
 ║   3406                                                ║  060e2b34.01010105.04010503.0b000000 - Statically Local Tags - Component Max Ref
 ║   3407                                                ║  060e2b34.01010105.04010503.0c000000 - Statically Local Tags - Component Min Ref
 ║   3B02                                                ║  060e2b34.01010102.07020110.02040000 - Statically Local Tags - Last Modified Date
 ║   3B03                                                ║  060e2b34.01010102.06010104.02010000 - Statically Local Tags - Content Storage
 ║   3B05                                                ║  060e2b34.01010102.03010201.05000000 - Statically Local Tags - Version
 ║   3B06                                                ║  060e2b34.01010102.06010104.06040000 - Statically Local Tags - Identifications
 ║   3B07                                                ║  060e2b34.01010102.03010201.04000000 - Statically Local Tags - Object Model Version
 ║   3B08                                                ║  060e2b34.01010104.06010104.01080000 - Statically Local Tags - Primary Package
 ║   3B09                                                ║  060e2b34.01010105.01020203.00000000 - Statically Local Tags - Operational Pattern
 ║   3B0A                                                ║  060e2b34.01010105.01020210.02010000 - Statically Local Tags - EssenceContainers
 ║   3B0B                                                ║  060e2b34.01010105.01020210.02020000 - Statically Local Tags - Descriptive Metadata (DM) Schemes
 ║   3C01                                                ║  060e2b34.01010102.05200701.02010000 - Statically Local Tags - Company Name
 ║   3C02                                                ║  060e2b34.01010102.05200701.03010000 - Statically Local Tags - Product Name
 ║   3C03                                                ║  060e2b34.01010102.05200701.04000000 - Statically Local Tags - Product Version
 ║   3C04                                                ║  060e2b34.01010102.05200701.05010000 - Statically Local Tags - Version String
 ║   3C05                                                ║  060e2b34.01010102.05200701.07000000 - Statically Local Tags - Product UID
 ║   3C06                                                ║  060e2b34.01010102.07020110.02030000 - Statically Local Tags - Modification Date
 ║   3C07                                                ║  060e2b34.01010102.05200701.0a000000 - Statically Local Tags - ToolkitVersion
 ║   3C08                                                ║  060e2b34.01010102.05200701.06010000 - Statically Local Tags - Platform
 ║   3C09                                                ║  060e2b34.01010102.05200701.01000000 - Statically Local Tags - This Generation UID
 ║   3C0A                                                ║  060e2b34.01010101.01011502.00000000 - Statically Local Tags - Instance UID
 ║   3F05                                                ║  060e2b34.01010104.04060201.00000000 - Statically Local Tags - Edit Unit Byte Count
 ║   3F06                                                ║  060e2b34.01010104.01030405.00000000 - Statically Local Tags - IndexSID
 ║   3F07                                                ║  060e2b34.01010104.01030404.00000000 - Statically Local Tags - BodySID
 ║   3F08                                                ║  060e2b34.01010104.04040401.01000000 - Statically Local Tags - Slice Count
 ║   3F09                                                ║  060e2b34.01010105.04040401.06000000 - Statically Local Tags - Delta Entry Array
 ║   3F0A                                                ║  060e2b34.01010105.04040402.05000000 - Statically Local Tags - Index Entry Array
 ║   3F0B                                                ║  060e2b34.01010105.05300406.00000000 - Statically Local Tags - Index Edit Rate
 ║   3F0C                                                ║  060e2b34.01010105.07020103.010a0000 - Statically Local Tags - Index Start Position
 ║   3F0D                                                ║  060e2b34.01010105.07020201.01020000 - Statically Local Tags - Index Duration
 ║   3F0E                                                ║  060e2b34.01010105.04040401.07000000 - Statically Local Tags - PosTableCount
 ║   4401                                                ║  060e2b34.01010101.01011510.00000000 - Statically Local Tags - Package UID
 ║   4402                                                ║  060e2b34.01010101.01030302.01000000 - Statically Local Tags - Name
 ║   4403                                                ║  060e2b34.01010102.06010104.06050000 - Statically Local Tags - Tracks UID
 ║   4404                                                ║  060e2b34.01010102.07020110.02050000 - Statically Local Tags - Package Modified Date
 ║   4405                                                ║  060e2b34.01010102.07020110.01030000 - Statically Local Tags - Package Creation Date
 ║   4701                                                ║  060e2b34.01010102.06010104.02030000 - Statically Local Tags - Descriptor
 ║   4801                                                ║  060e2b34.01010102.01070101.00000000 - Statically Local Tags - Track ID
 ║   4802                                                ║  060e2b34.01010102.01070102.01000000 - Statically Local Tags - Track Name
 ║   4803                                                ║  060e2b34.01010102.06010104.02040000 - Statically Local Tags - Sequence UID
 ║   4804                                                ║  060e2b34.01010102.01040103.00000000 - Statically Local Tags - Track Number
 ║   4B01                                                ║  060e2b34.01010102.05300405.00000000 - Statically Local Tags - Edit Rate
 ║   4B02                                                ║  060e2b34.01010102.07020103.01030000 - Statically Local Tags - Origin
 ║   FFF2                                                ║  060e2b34.0101010a.04010603.0d000000 - Dynamically Local Tags - Quantization Default
 ║   FFF3                                                ║  060e2b34.0101010a.04010603.0c000000 - Dynamically Local Tags - Coding Style Default
 ║   FFF4                                                ║  060e2b34.0101010a.04010603.0b000000 - Dynamically Local Tags - Picture Component Sizing
 ║   FFF5                                                ║  060e2b34.0101010a.04010603.0a000000 - Dynamically Local Tags - Csiz - Number Components
 ║   FFF6                                                ║  060e2b34.0101010a.04010603.09000000 - Dynamically Local Tags - YTOsiz - Vertical Offset Tile
 ║   FFF7                                                ║  060e2b34.0101010a.04010603.08000000 - Dynamically Local Tags - XTOsiz - Horizontal Offset Tile
 ║   FFF8                                                ║  060e2b34.0101010a.04010603.07000000 - Dynamically Local Tags - YTsiz - Height Reference Tile
 ║   FFF9                                                ║  060e2b34.0101010a.04010603.06000000 - Dynamically Local Tags - XTsiz - Width Reference Tile
 ║   FFFA                                                ║  060e2b34.0101010a.04010603.05000000 - Dynamically Local Tags - YOsiz - Vertical Offset Ysiz
 ║   FFFB                                                ║  060e2b34.0101010a.04010603.04000000 - Dynamically Local Tags - XOsiz - Horizontal Offset Xsiz
 ║   FFFC                                                ║  060e2b34.0101010a.04010603.03000000 - Dynamically Local Tags - Ysiz - Height Reference Grid
 ║   FFFD                                                ║  060e2b34.0101010a.04010603.02000000 - Dynamically Local Tags - Xsiz - Width Reference Grid
 ║   FFFE                                                ║  060e2b34.0101010a.04010603.01000000 - Dynamically Local Tags - Rsiz - Capabilities Code
 ║   FFFF                                                ║  060e2b34.01010109.06010104.06100000 - Dynamically Local Tags - Descriptors & Sub-Descriptors (SMPTE)
 ║   Resource [1]                                        ║  SMPTE ST 377-1:2011 - MXF - File Format Specification - Page 55 - (Table 13)
 ║   Parser                                              ║  primer_pack
 ║   Data - Key                                          ║  060e2b34020501010d01020101050100
 ║   Data - Length                                       ║  000596 (1430 bytes)
 ║   Data - Value [0]                                    ║  0000004f000000120201060e2b340101010204070100000000000202060e2b34010101020702
 ║   Data - Value [1]                                    ║  0201010300001001060e2b340101010206010104060900001101060e2b340101010206010103
 ║   Data - Value [2]                                    ║  010000001102060e2b340101010206010103020000001201060e2b3401010102070201030104
 ║   Data - Value [3]                                    ║  00001501060e2b340101010207020103010500001502060e2b34010101020404010102060000
 ║   Data - Value [4]                                    ║  1503060e2b340101010104040101050000001901060e2b340101010206010104050100001902
 ║   Data - Value [5]                                    ║  060e2b340101010206010104050200002701060e2b340101010206010106010000003001060e
 ║   Data - Value [6]                                    ║  (31 more...)
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	1590 │ 060e2b34.02530101.0d010101.01012f00 │ 83.0000be	:	       190 │ 3c0a0010aaffbd07420e44a2b3f87d3c │ Preface
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  aaffbd07.420e44a2.b3f87d3c.aaa44c3d
 ║   3B02 - Last Modified Date                           ║  2022-04-08 22:01:50.0000+00:00
 ║   3B05 - Version                                      ║  258
 ║   3B07 - Object Model Version                         ║  1
 ║   3B08 - Primary Package                              ║  b87f0871.f98446d3.9a842893.47b298fc
 ║   3B06 - Identifications                              ║  1 item(s): c00c5d91.bc1b4e58.aefabf33.99a2d6f9
 ║   3B03 - Content Storage                              ║  acc6d12c.da0c465b.861a1c33.7abbc330
 ║   3B09 - Operational Pattern                          ║  060e2b34.04010102.0d010201.10000000	(Operational Pattern - Specialized Pattern - OP Atom - SMPTE)
 ║   3B0A - EssenceContainers                            ║  2 item(s): 060e2b34.04010103.0d010301.027f0100, 060e2b34.04010107.0d010301.020c0100
 ║   3B0B - Descriptive Metadata (DM) Schemes            ║  0 item(s): 
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 113
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101012f00
 ║   Data - Length                                       ║  0000be (190 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010aaffbd07420e44a2b3f87d3caaa44c3d3b02000807e60408160132003b0500020102
 ║   Data - Value [1]                                    ║  3b070004000000013b080010b87f0871f98446d39a84289347b298fc3b060018000000010000
 ║   Data - Value [2]                                    ║  0010c00c5d91bc1b4e58aefabf3399a2d6f93b030010acc6d12cda0c465b861a1c337abbc330
 ║   Data - Value [3]                                    ║  3b090010060e2b34040101020d010201100000003b0a00280000000200000010060e2b340401
 ║   Data - Value [4]                                    ║  01030d010301027f0100060e2b34040101070d010301020c01003b0b00080000000000000010
 ║   Data - Value [5]                                    ║  
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	1800 │ 060e2b34.02530101.0d010101.01013000 │ 83.0000d8	:	       216 │ 3c0a0010c00c5d91bc1b4e58aefabf33 │ Identification
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  c00c5d91.bc1b4e58.aefabf33.99a2d6f9
 ║   3C09 - This Generation UID                          ║  e843f4f0.82754f28.ad287b0c.f7bd3d19
 ║   3C01 - Company Name                                 ║  WidgetCo
 ║   3C02 - Product Name                                 ║  asdcp-test
 ║   3C03 - Product Version                              ║  0.0.0.0.0
 ║   3C04 - Version String                               ║  2.10.35
 ║   3C05 - Product UID                                  ║  7d836e16.37c74c22.b2e046a7.17e84f42
 ║   3C06 - Modification Date                            ║  2022-04-08 22:01:50.0000+00:00
 ║   3C07 - ToolkitVersion                               ║  2.10.35.27240.1
 ║   3C08 - Platform                                     ║  x86_64-apple-darwin15.6.0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 73 + 114
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013000
 ║   Data - Length                                       ║  0000d8 (216 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010c00c5d91bc1b4e58aefabf3399a2d6f93c090010e843f4f082754f28ad287b0cf7bd
 ║   Data - Value [1]                                    ║  3d193c0100100057006900640067006500740043006f3c02001400610073006400630070002d
 ║   Data - Value [2]                                    ║  00740065007300743c03000a000000000000000000003c04000e0032002e00310030002e0033
 ║   Data - Value [3]                                    ║  00353c0500107d836e1637c74c22b2e046a717e84f423c06000807e60408160132003c07000a
 ║   Data - Value [4]                                    ║  0002000a00236a6800013c080032007800380036005f00360034002d006100700070006c0065
 ║   Data - Value [5]                                    ║  002d00640061007200770069006e00310035002e0036002e0030
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2036 │ 060e2b34.02530101.0d010101.01011800 │ 83.00005c	:	        92 │ 3c0a0010acc6d12cda0c465b861a1c33 │ Content Storage
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  acc6d12c.da0c465b.861a1c33.7abbc330
 ║   1901 - Packages                                     ║  2 item(s): 96b13153.bd5d4cd2.9abcd608.f12df054, b87f0871.f98446d3.9a842893.47b298fc
 ║   1902 - Essence Container Data                       ║  1 item(s): bf8a6ebc.3aca4164.a47e45e0.4caef4f7
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 116
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101011800
 ║   Data - Length                                       ║  00005c (92 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010acc6d12cda0c465b861a1c337abbc33019010028000000020000001096b13153bd5d
 ║   Data - Value [1]                                    ║  4cd29abcd608f12df054b87f0871f98446d39a84289347b298fc190200180000000100000010
 ║   Data - Value [2]                                    ║  bf8a6ebc3aca4164a47e45e04caef4f7
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2148 │ 060e2b34.02530101.0d010101.01012300 │ 83.000048	:	        72 │ 3c0a0010bf8a6ebc3aca4164a47e45e0 │ Essence Container Data
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  bf8a6ebc.3aca4164.a47e45e0.4caef4f7
 ║   2701 - Linked Package UID                           ║  UL:060a2b34.01010105.01010f20, Length:13 (Basic UMID Format), Instance:000000, Materiel:c6ba4b61.34834c90.a518b6d6.50ac9605
 ║   3F06 - IndexSID                                     ║  129
 ║   3F07 - BodySID                                      ║  1
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 116
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101012300
 ║   Data - Length                                       ║  000048 (72 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010bf8a6ebc3aca4164a47e45e04caef4f727010020060a2b340101010501010f201300
 ║   Data - Value [1]                                    ║  0000c6ba4b6134834c90a518b6d650ac96053f060004000000813f07000400000001
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2240 │ 060e2b34.02530101.0d010101.01013600 │ 83.0000a0	:	       160 │ 3c0a001096b13153bd5d4cd29abcd608 │ Material Package
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  96b13153.bd5d4cd2.9abcd608.f12df054
 ║   4401 - Package UID                                  ║  UL:060a2b34.01010105.01010f20, Length:13 (Basic UMID Format), Instance:000000, Materiel:68048603.0b8a4300.a48fedf1.308fecfe
 ║   4402 - Name                                         ║  Material Package
 ║   4405 - Package Creation Date                        ║  2022-04-08 22:01:50.0000+00:00
 ║   4404 - Package Modified Date                        ║  2022-04-08 22:01:50.0000+00:00
 ║   4403 - Tracks UID                                   ║  2 item(s): 005ea82d.6afb4a37.aae4d74b.c1ea2528, f8427198.af884d4f.8c9855f3.fa43f66e
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 117 - Generic Package table
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013600
 ║   Data - Length                                       ║  0000a0 (160 bytes)
 ║   Data - Value [0]                                    ║  3c0a001096b13153bd5d4cd29abcd608f12df05444010020060a2b340101010501010f201300
 ║   Data - Value [1]                                    ║  0000680486030b8a4300a48fedf1308fecfe44020020004d006100740065007200690061006c
 ║   Data - Value [2]                                    ║  0020005000610063006b0061006700654405000807e60408160132004404000807e604081601
 ║   Data - Value [3]                                    ║  3200440300280000000200000010005ea82d6afb4a37aae4d74bc1ea2528f8427198af884d4f
 ║   Data - Value [4]                                    ║  8c9855f3fa43f66e
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2420 │ 060e2b34.02530101.0d010101.01013b00 │ 83.000070	:	       112 │ 3c0a0010005ea82d6afb4a37aae4d74b │ Timeline Track
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  005ea82d.6afb4a37.aae4d74b.c1ea2528
 ║   4801 - Track ID                                     ║  1
 ║   4804 - Track Number                                 ║  00000000
 ║   4802 - Track Name                                   ║  Timecode Track
 ║   4803 - Sequence UID                                 ║  8afb9187.a608464f.85713462.8b475279
 ║   4B01 - Edit Rate                                    ║  24/1
 ║   4B02 - Origin                                       ║  0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timeline Track  (B.6 Generic Track - page 119 + B.15 Timeline Track (Timecode) - page 124)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013b00
 ║   Data - Length                                       ║  000070 (112 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010005ea82d6afb4a37aae4d74bc1ea2528480100040000000148040004000000004802
 ║   Data - Value [1]                                    ║  001c00540069006d00650063006f0064006500200054007200610063006b480300108afb9187
 ║   Data - Value [2]                                    ║  a608464f857134628b4752794b01000800000018000000014b0200080000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2552 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a00108afb9187a608464f85713462 │ Sequence
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  8afb9187.a608464f.85713462.8b475279
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030201.01000000	(Timecode Track (with inactive user bits))
 ║   0202 - Duration                                     ║  1
 ║   1001 - Structural Components UID                    ║  1 item(s): 8fe911af.95d4464e.9e794651.0434a0c5
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Sequence (B.16 Sequence (Timecode) - page 125 + B9 + B8)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101010f00
 ║   Data - Length                                       ║  000050 (80 bytes)
 ║   Data - Value [0]                                    ║  3c0a00108afb9187a608464f857134628b47527902010010060e2b3404010101010302010100
 ║   Data - Value [1]                                    ║  00000202000800000000000000011001001800000001000000108fe911af95d4464e9e794651
 ║   Data - Value [2]                                    ║  0434a0c5
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2652 │ 060e2b34.02530101.0d010101.01011400 │ 83.00004b	:	        75 │ 3c0a00108fe911af95d4464e9e794651 │ Timecode Component
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  8fe911af.95d4464e.9e794651.0434a0c5
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030201.01000000	(Timecode Track (with inactive user bits))
 ║   0202 - Duration                                     ║  1
 ║   1502 - Rounded Timecode Base                        ║  24
 ║   1501 - Start Timecode                               ║  0
 ║   1503 - Drop Frame                                   ║  False
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timecode Component
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101011400
 ║   Data - Length                                       ║  00004b (75 bytes)
 ║   Data - Value [0]                                    ║  3c0a00108fe911af95d4464e9e7946510434a0c502010010060e2b3404010101010302010100
 ║   Data - Value [1]                                    ║  00000202000800000000000000011502000200181501000800000000000000001503000100
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2747 │ 060e2b34.02530101.0d010101.01013b00 │ 83.00006e	:	       110 │ 3c0a0010f8427198af884d4f8c9855f3 │ Timeline Track
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  f8427198.af884d4f.8c9855f3.fa43f66e
 ║   4801 - Track ID                                     ║  2
 ║   4804 - Track Number                                 ║  00000000
 ║   4802 - Track Name                                   ║  Picture Track
 ║   4803 - Sequence UID                                 ║  e2bfd055.e5d249a0.bfcb4da8.a4456b01
 ║   4B01 - Edit Rate                                    ║  24/1
 ║   4B02 - Origin                                       ║  0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timeline Track  (B.6 Generic Track - page 119 + B.15 Timeline Track (Timecode) - page 124)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013b00
 ║   Data - Length                                       ║  00006e (110 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010f8427198af884d4f8c9855f3fa43f66e480100040000000248040004000000004802
 ║   Data - Value [1]                                    ║  001a005000690063007400750072006500200054007200610063006b48030010e2bfd055e5d2
 ║   Data - Value [2]                                    ║  49a0bfcb4da8a4456b014b01000800000018000000014b0200080000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2877 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a0010e2bfd055e5d249a0bfcb4da8 │ Sequence
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  e2bfd055.e5d249a0.bfcb4da8.a4456b01
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030202.01000000	(Picture Essence Track)
 ║   0202 - Duration                                     ║  1
 ║   1001 - Structural Components UID                    ║  1 item(s): 6daf21ba.b69a41c9.9ec54f4f.589a0dec
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Sequence (B.16 Sequence (Timecode) - page 125 + B9 + B8)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101010f00
 ║   Data - Length                                       ║  000050 (80 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010e2bfd055e5d249a0bfcb4da8a4456b0102010010060e2b3404010101010302020100
 ║   Data - Value [1]                                    ║  00000202000800000000000000011001001800000001000000106daf21bab69a41c99ec54f4f
 ║   Data - Value [2]                                    ║  589a0dec
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	2977 │ 060e2b34.02530101.0d010101.01011100 │ 83.00006c	:	       108 │ 3c0a00106daf21bab69a41c99ec54f4f │ Source Clip
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  6daf21ba.b69a41c9.9ec54f4f.589a0dec
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030202.01000000	(Picture Essence Track)
 ║   0202 - Duration                                     ║  1
 ║   1201 - Start Position                               ║  0
 ║   1101 - SourcePackageID                              ║  UL:060a2b34.01010105.01010f20, Length:13 (Basic UMID Format), Instance:000000, Materiel:c6ba4b61.34834c90.a518b6d6.50ac9605
 ║   1102 - SourceTrackID                                ║  2
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 122+127
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101011100
 ║   Data - Length                                       ║  00006c (108 bytes)
 ║   Data - Value [0]                                    ║  3c0a00106daf21bab69a41c99ec54f4f589a0dec02010010060e2b3404010101010302020100
 ║   Data - Value [1]                                    ║  000002020008000000000000000112010008000000000000000011010020060a2b3401010105
 ║   Data - Value [2]                                    ║  01010f2013000000c6ba4b6134834c90a518b6d650ac96051102000400000002
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3105 │ 060e2b34.02530101.0d010101.01013700 │ 83.000116	:	       278 │ 3c0a0010b87f0871f98446d39a842893 │ Source Package
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  b87f0871.f98446d3.9a842893.47b298fc
 ║   4401 - Package UID                                  ║  UL:060a2b34.01010105.01010f20, Length:13 (Basic UMID Format), Instance:000000, Materiel:c6ba4b61.34834c90.a518b6d6.50ac9605
 ║   4402 - Name                                         ║  File Package: SMPTE 429-4 frame wrapping of JPEG 2000 codestreams
 ║   4405 - Package Creation Date                        ║  2022-04-08 22:01:50.0000+00:00
 ║   4404 - Package Modified Date                        ║  2022-04-08 22:01:50.0000+00:00
 ║   4403 - Tracks UID                                   ║  2 item(s): 6378d221.8be746d2.8508fedf.1d4bed62, d4e73370.0afb4532.9cc796c6.933766d5
 ║   4701 - Descriptor                                   ║  2cb46505.be6b41c3.abbe8848.d06e21c9
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013700
 ║   Data - Length                                       ║  000116 (278 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010b87f0871f98446d39a84289347b298fc44010020060a2b340101010501010f201300
 ║   Data - Value [1]                                    ║  0000c6ba4b6134834c90a518b6d650ac96054402008200460069006c00650020005000610063
 ║   Data - Value [2]                                    ║  006b006100670065003a00200053004d0050005400450020003400320039002d003400200066
 ║   Data - Value [3]                                    ║  00720061006d00650020007700720061007000700069006e00670020006f00660020004a0050
 ║   Data - Value [4]                                    ║  004500470020003200300030003000200063006f0064006500730074007200650061006d0073
 ║   Data - Value [5]                                    ║  4405000807e60408160132004404000807e60408160132004403002800000002000000106378
 ║   Data - Value [6]                                    ║  (1 more...)
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3403 │ 060e2b34.02530101.0d010101.01013b00 │ 83.000070	:	       112 │ 3c0a00106378d2218be746d28508fedf │ Timeline Track
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  6378d221.8be746d2.8508fedf.1d4bed62
 ║   4801 - Track ID                                     ║  1
 ║   4804 - Track Number                                 ║  00000000
 ║   4802 - Track Name                                   ║  Timecode Track
 ║   4803 - Sequence UID                                 ║  75ef5360.6937484a.9ee14472.93647966
 ║   4B01 - Edit Rate                                    ║  24/1
 ║   4B02 - Origin                                       ║  0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timeline Track  (B.6 Generic Track - page 119 + B.15 Timeline Track (Timecode) - page 124)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013b00
 ║   Data - Length                                       ║  000070 (112 bytes)
 ║   Data - Value [0]                                    ║  3c0a00106378d2218be746d28508fedf1d4bed62480100040000000148040004000000004802
 ║   Data - Value [1]                                    ║  001c00540069006d00650063006f0064006500200054007200610063006b4803001075ef5360
 ║   Data - Value [2]                                    ║  6937484a9ee14472936479664b01000800000018000000014b0200080000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3535 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a001075ef53606937484a9ee14472 │ Sequence
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  75ef5360.6937484a.9ee14472.93647966
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030201.01000000	(Timecode Track (with inactive user bits))
 ║   0202 - Duration                                     ║  1
 ║   1001 - Structural Components UID                    ║  1 item(s): 59cf1ad8.6f314b5d.b0164871.d32bea4e
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Sequence (B.16 Sequence (Timecode) - page 125 + B9 + B8)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101010f00
 ║   Data - Length                                       ║  000050 (80 bytes)
 ║   Data - Value [0]                                    ║  3c0a001075ef53606937484a9ee144729364796602010010060e2b3404010101010302010100
 ║   Data - Value [1]                                    ║  000002020008000000000000000110010018000000010000001059cf1ad86f314b5db0164871
 ║   Data - Value [2]                                    ║  d32bea4e
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3635 │ 060e2b34.02530101.0d010101.01011400 │ 83.00004b	:	        75 │ 3c0a001059cf1ad86f314b5db0164871 │ Timecode Component
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  59cf1ad8.6f314b5d.b0164871.d32bea4e
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030201.01000000	(Timecode Track (with inactive user bits))
 ║   0202 - Duration                                     ║  1
 ║   1502 - Rounded Timecode Base                        ║  24
 ║   1501 - Start Timecode                               ║  0
 ║   1503 - Drop Frame                                   ║  False
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timecode Component
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101011400
 ║   Data - Length                                       ║  00004b (75 bytes)
 ║   Data - Value [0]                                    ║  3c0a001059cf1ad86f314b5db0164871d32bea4e02010010060e2b3404010101010302010100
 ║   Data - Value [1]                                    ║  00000202000800000000000000011502000200181501000800000000000000001503000100
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3730 │ 060e2b34.02530101.0d010101.01013b00 │ 83.00006e	:	       110 │ 3c0a0010d4e733700afb45329cc796c6 │ Timeline Track
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  d4e73370.0afb4532.9cc796c6.933766d5
 ║   4801 - Track ID                                     ║  2
 ║   4804 - Track Number                                 ║  15010801
 ║   4802 - Track Name                                   ║  Picture Track
 ║   4803 - Sequence UID                                 ║  e2f035aa.64684a7f.98eddfa7.87e08a67
 ║   4B01 - Edit Rate                                    ║  24/1
 ║   4B02 - Origin                                       ║  0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Timeline Track  (B.6 Generic Track - page 119 + B.15 Timeline Track (Timecode) - page 124)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101013b00
 ║   Data - Length                                       ║  00006e (110 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010d4e733700afb45329cc796c6933766d5480100040000000248040004150108014802
 ║   Data - Value [1]                                    ║  001a005000690063007400750072006500200054007200610063006b48030010e2f035aa6468
 ║   Data - Value [2]                                    ║  4a7f98eddfa787e08a674b01000800000018000000014b0200080000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3860 │ 060e2b34.02530101.0d010101.01010f00 │ 83.000050	:	        80 │ 3c0a0010e2f035aa64684a7f98eddfa7 │ Sequence
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  e2f035aa.64684a7f.98eddfa7.87e08a67
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030202.01000000	(Picture Essence Track)
 ║   0202 - Duration                                     ║  1
 ║   1001 - Structural Components UID                    ║  1 item(s): c93d2257.b09a4dbe.a24c782e.f9b3ef4a
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Sequence (B.16 Sequence (Timecode) - page 125 + B9 + B8)
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101010f00
 ║   Data - Length                                       ║  000050 (80 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010e2f035aa64684a7f98eddfa787e08a6702010010060e2b3404010101010302020100
 ║   Data - Value [1]                                    ║  0000020200080000000000000001100100180000000100000010c93d2257b09a4dbea24c782e
 ║   Data - Value [2]                                    ║  f9b3ef4a
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	3960 │ 060e2b34.02530101.0d010101.01011100 │ 83.00006c	:	       108 │ 3c0a0010c93d2257b09a4dbea24c782e │ Source Clip
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  c93d2257.b09a4dbe.a24c782e.f9b3ef4a
 ║   0201 - Data Definition                              ║  060e2b34.04010101.01030202.01000000	(Picture Essence Track)
 ║   0202 - Duration                                     ║  1
 ║   1201 - Start Position                               ║  0
 ║   1101 - SourcePackageID                              ║  UL:00000000.00000000.00000000, Length:00 (Unknown UMID Format), Instance:000000, Materiel:00000000.00000000.00000000.00000000
 ║   1102 - SourceTrackID                                ║  0
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 122+127
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101011100
 ║   Data - Length                                       ║  00006c (108 bytes)
 ║   Data - Value [0]                                    ║  3c0a0010c93d2257b09a4dbea24c782ef9b3ef4a02010010060e2b3404010101010302020100
 ║   Data - Value [1]                                    ║  0000020200080000000000000001120100080000000000000000110100200000000000000000
 ║   Data - Value [2]                                    ║  0000000000000000000000000000000000000000000000001102000400000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	4088 │ 060e2b34.02530101.0d010101.01012900 │ 83.0000bd	:	       189 │ 3c0a00102cb46505be6b41c3abbe8848 │ RGBA Essence Descriptor
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  2cb46505.be6b41c3.abbe8848.d06e21c9
 ║   FFFF - Descriptors & Sub-Descriptors (SMPTE)        ║  1 item(s): 6054268f.8fdf47ba.98db7167.5d3f704b
 ║   3006 - Linked Track ID                              ║  2
 ║   3001 - Sample Rate                                  ║  24/1
 ║   3002 - Container Duration                           ║  1
 ║   3004 - Essence Container                            ║  060e2b34.04010107.0d010301.020c0100	(JPEG2000 Picture Element - Frame Wrapped)
 ║   320C - Frame Layout                                 ║  FULL_FRAME (0)
 ║   3203 - Stored Width                                 ║  4096
 ║   3202 - Stored Height                                ║  2160
 ║   320E - Aspect Ratio                                 ║  4096/2160 (1.90)
 ║   3201 - Picture Essence Coding                       ║  JPEG 2000 4K Digital Cinema Profile (060e2b34040101090401020203010104)
 ║   3406 - Component Max Ref                            ║  4095
 ║   3407 - Component Min Ref                            ║  0
 ║   3401 - PixelLayout                                  ║  8 item(s): Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes, Termination - 0 bytes
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 148
 ║   Resource [2]                                        ║  SMPTE.ST.0429-4-2006 - DCP - MXF JPEG2000 Application
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101012900
 ║   Data - Length                                       ║  0000bd (189 bytes)
 ║   Data - Value [0]                                    ║  3c0a00102cb46505be6b41c3abbe8848d06e21c9ffff001800000001000000106054268f8fdf
 ║   Data - Value [1]                                    ║  47ba98db71675d3f704b30060004000000023001000800000018000000013002000800000000
 ║   Data - Value [2]                                    ║  0000000130040010060e2b34040101070d010301020c0100320c000100320300040000100032
 ║   Data - Value [3]                                    ║  02000400000870320e0008000010000000087032010010060e2b340401010904010202030101
 ║   Data - Value [4]                                    ║  043406000400000fff34070004000000003401001000000000000000000000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	4297 │ 060e2b34.02530101.0d010101.01015a00 │ 83.0000b5	:	       181 │ 3c0a00106054268f8fdf47ba98db7167 │ JPEG2000 Picture Sub-Descriptor
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  6054268f.8fdf47ba.98db7167.5d3f704b
 ║   FFFE - Rsiz - Capabilities Code                     ║  4
 ║   FFFD - Xsiz - Width Reference Grid                  ║  4096
 ║   FFFC - Ysiz - Height Reference Grid                 ║  2160
 ║   FFFB - XOsiz - Horizontal Offset Xsiz               ║  0
 ║   FFFA - YOsiz - Vertical Offset Ysiz                 ║  0
 ║   FFF9 - XTsiz - Width Reference Tile                 ║  4096
 ║   FFF8 - YTsiz - Height Reference Tile                ║  2160
 ║   FFF7 - XTOsiz - Horizontal Offset Tile              ║  0
 ║   FFF6 - YTOsiz - Vertical Offset Tile                ║  0
 ║   FFF5 - Csiz - Number Components                     ║  3
 ║   FFF4 - Picture Component Sizing                     ║  3 elements (3 bytes each) => {Ssiz : 11 (0x0b), XRSiz : 1 (0x01), YRSiz : 1 (0x01)}, {Ssiz : 11 (0x0b), XRSiz : 1 (0x01), YRSiz : 1 (0x01)}, {Ssiz : 11 (0x0b), XRSiz : 1 (0x01), YRSiz : 1 (0x01)}
 ║   FFF3 - Coding Style Default                         ║  Scod:0x01, SGcod-ProgressionOrder:0x04, SGcod-NumberLayers:0x0001, SGcod-MultipleComponentTransformation:0x01, SPcod-NumberOfDecompositionLevels:0x06, SPcod-CodeBlock-Width:0x03, SPcod-CodeBlock-Height:0x03, SPcod-CodeBlock-Style:0x00, SPcod-WaveletTransformation:0x00 (Irreversible), SPcod-PrecinctSizeSubband:0x77, SPcod-PrecinctSizeResolutionsLevels: 6 elements => 0x88, 0x88, 0x88, 0x88, 0x88, 0x88
 ║   FFF2 - Quantization Default                         ║  Sqcd-all:0x42, Sqcd[1]:0x7f34, Sqcd[2]:0x7ef1, Sqcd[3]:0x7ef1, Sqcd[4]:0x7eae, Sqcd[5]:0x76f1, Sqcd[6]:0x76f1, Sqcd[7]:0x76ae, Sqcd[8]:0x6f02, Sqcd[9]:0x6f02, Sqcd[10]:0x6ee0, Sqcd[11]:0x674d, Sqcd[12]:0x674d, Sqcd[13]:0x6767, Sqcd[14]:0x5003, Sqcd[15]:0x5003, Sqcd[16]:0x5044, Sqcd[17]:0x57d2, Sqcd[18]:0x57d2, Sqcd[19]:0x5760
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - Generic Picture Essence Descriptor
 ║   Resource [2]                                        ║  SMPTE.ST.0429-4-2006 - DCP - MXF JPEG2000 Application
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01010101015a00
 ║   Data - Length                                       ║  0000b5 (181 bytes)
 ║   Data - Value [0]                                    ║  3c0a00106054268f8fdf47ba98db71675d3f704bfffe00020004fffd000400001000fffc0004
 ║   Data - Value [1]                                    ║  00000870fffb000400000000fffa000400000000fff9000400001000fff8000400000870fff7
 ║   Data - Value [2]                                    ║  000400000000fff6000400000000fff500020003fff4001100000003000000030b01010b0101
 ║   Data - Value [3]                                    ║  0b0101fff300110104000101060303000077888888888888fff20027427f347ef17ef17eae76
 ║   Data - Value [4]                                    ║  f176f176ae6f026f026ee0674d674d676750035003504457d257d25760
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
	4498 │ 060e2b34.01010102.03010210.01000000 │ 83.002e5a	:	     11866 │ 00000000000000000000000000000000 │ KLV Fill item (SMPTE)
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Data                                                ║  00000000000000000000000000000000…00000000000000000000000000000000
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - KLV Fill item
 ║   Parser                                              ║  fill_item
 ║   Data - Key                                          ║  060e2b34010101020301021001000000
 ║   Data - Length                                       ║  002e5a (11866 bytes)
 ║   Data - Value [0]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [1]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [2]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [3]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [4]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [5]                                    ║  0000000000000000000000000000000000000000000000000000000000000000000000000000
 ║   Data - Value [6]                                    ║  (306 more...)
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   16384 │ 060e2b34.02050101.0d010201.01030400 │ 83.000078	:	       120 │ 00010002000000010000000000004000 │ Partition Pack - Body - Closed & Complete
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Major Version                                       ║  1
 ║   Minor Version                                       ║  2
 ║   KAGSize                                             ║  1
 ║   ThisPartition                                       ║  16384
 ║   PreviousPartition                                   ║  0
 ║   FooterPartition                                     ║  0
 ║   HeaderByteCount                                     ║  0
 ║   IndexByteCount                                      ║  0
 ║   IndexSID                                            ║  0
 ║   BodyOffset                                          ║  0
 ║   BodySID                                             ║  1
 ║   Operational Pattern                                 ║  060e2b34.04010102.0d010201.10000000	(Operational Pattern - Specialized Pattern - OP Atom - SMPTE)
 ║   EssenceContainers                                   ║  2 item(s): 060e2b34.04010103.0d010301.027f0100, 060e2b34.04010107.0d010301.020c0100
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 45
 ║   Parser                                              ║  partition_pack
 ║   Data - Key                                          ║  060e2b34020501010d01020101030400
 ║   Data - Length                                       ║  000078 (120 bytes)
 ║   Data - Value [0]                                    ║  0001000200000001000000000000400000000000000000000000000000000000000000000000
 ║   Data - Value [1]                                    ║  0000000000000000000000000000000000000000000000000001060e2b34040101020d010201
 ║   Data - Value [2]                                    ║  100000000000000200000010060e2b34040101030d010301027f0100060e2b34040101070d01
 ║   Data - Value [3]                                    ║  0301020c0100
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   16524 │ 060e2b34.01020101.0d010301.15010801 │ 83.009cc8	:	     40136 │ ff4fff51002f00040000100000000870 │ Picture Essence - 1 frame
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Type                                                ║  Plaintext JPEG2000
 ║   Data                                                ║  ff4fff51002f00040000100000000870…8080808080808080808080808080ffd9
 ║   JPEG2000 Header                                     ║  └──────┘ found here
 ║   JPEG2000 Metadata                                   ║  (....)
 ║   Resource [1]                                        ║  SMPTE.ST.0422-2014 - MXF - Mapping JPEG2000 Codestreams into the MXF Generic Container
 ║   Resource [2]                                        ║  SMPTE.ST.0429-4-2006 - DCP - MXF JPEG2000 Application
 ║   Resource [3]                                        ║  SMPTE.ST.0384M-2005 - TV - MXF - Mapping of Uncompressed Pictures into the Generic Container
 ║   Parser                                              ║  picture_essence
 ║   Data - Key                                          ║  060e2b34010201010d01030115010801
 ║   Data - Length                                       ║  009cc8 (40136 bytes)
 ║   Data - Value [0]                                    ║  ff4fff51002f0004000010000000087000000000000000000000100000000870000000000000
 ║   Data - Value [1]                                    ║  000000030b01010b01010b0101ff5200130104000101060303000077888888888888ff5c0029
 ║   Data - Value [2]                                    ║  427f347ef17ef17eae76f176f176ae6f026f026ee0674d674d676750035003504457d257d257
 ║   Data - Value [3]                                    ║  60ff5f00100000000106030406000001070304ff550022005000000043e100000014a9000000
 ║   Data - Value [4]                                    ║  0caf0000002ecc000000063900000001b5ff6400280001437265617465642077697468204456
 ║   Data - Value [5]                                    ║  5320436c69707374657220352e31302e302e313400ff90000a0000000043e10006ff93e7ff00
 ║   Data - Value [6]                                    ║  (1050 more...)
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   56680 │ 060e2b34.02050101.0d010201.01040400 │ 83.000078	:	       120 │ 0001000200000001000000000000dd68 │ Partition Pack - Footer - Closed & Complete
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Major Version                                       ║  1
 ║   Minor Version                                       ║  2
 ║   KAGSize                                             ║  1
 ║   ThisPartition                                       ║  56680
 ║   PreviousPartition                                   ║  16384
 ║   FooterPartition                                     ║  56680
 ║   HeaderByteCount                                     ║  0
 ║   IndexByteCount                                      ║  151
 ║   IndexSID                                            ║  129
 ║   BodyOffset                                          ║  0
 ║   BodySID                                             ║  0
 ║   Operational Pattern                                 ║  060e2b34.04010102.0d010201.10000000	(Operational Pattern - Specialized Pattern - OP Atom - SMPTE)
 ║   EssenceContainers                                   ║  2 item(s): 060e2b34.04010103.0d010301.027f0100, 060e2b34.04010107.0d010301.020c0100
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 45
 ║   Parser                                              ║  partition_pack
 ║   Data - Key                                          ║  060e2b34020501010d01020101040400
 ║   Data - Length                                       ║  000078 (120 bytes)
 ║   Data - Value [0]                                    ║  0001000200000001000000000000dd680000000000004000000000000000dd68000000000000
 ║   Data - Value [1]                                    ║  0000000000000000009700000081000000000000000000000000060e2b34040101020d010201
 ║   Data - Value [2]                                    ║  100000000000000200000010060e2b34040101030d010301027f0100060e2b34040101070d01
 ║   Data - Value [3]                                    ║  0301020c0100
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   56820 │ 060e2b34.02530101.0d010201.01100100 │ 83.000083	:	       131 │ 3c0a00101c86aa0136fb414ebcd47120 │ Index Table Segment (2-bytes LocalTags, 2-bytes Length)
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   3C0A - Instance UID                                 ║  1c86aa01.36fb414e.bcd47120.5ba6f4df
 ║   3F0B - Index Edit Rate                              ║  24/1
 ║   3F0C - Index Start Position                         ║  0
 ║   3F0D - Index Duration                               ║  1
 ║   3F05 - Edit Unit Byte Count                         ║  0
 ║   3F06 - IndexSID                                     ║  129
 ║   3F07 - BodySID                                      ║  1
 ║   3F08 - Slice Count                                  ║  0
 ║   3F0E - PosTableCount                                ║  0
 ║   3F09 - Delta Entry Array                            ║  1 entries (6 bytes each)
 ║   3F0A - Index Entry Array                            ║  1 entries (11 bytes each)
 ║   Resource [1]                                        ║  SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 102
 ║   Parser                                              ║  klv
 ║   Data - Key                                          ║  060e2b34025301010d01020101100100
 ║   Data - Length                                       ║  000083 (131 bytes)
 ║   Data - Value [0]                                    ║  3c0a00101c86aa0136fb414ebcd471205ba6f4df3f0b000800000018000000013f0c00080000
 ║   Data - Value [1]                                    ║  0000000000003f0d000800000000000000013f050004000000003f060004000000813f070004
 ║   Data - Value [2]                                    ║  000000013f080001003f0e0001003f09000e00000001000000060000000000003f0a00130000
 ║   Data - Value [3]                                    ║  00010000000b0000800000000000000000
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
27 KLV found in MXF
```




### Read specific KLV (filter mode)

```
$ python -m mxf_reader -f tests/assets/2D.mxf --filter "Picture Essence" -vv
```

Output : 

```
Filename tests/assets/2D.mxf (57031 bytes)
610 SMPTE Universal Labels loaded
162 SMPTE Local Tags loaded
  offset │ uuid                                │ ber      	:	 data-size │                             data │ name
   16524 │ 060e2b34.01020101.0d010301.15010801 │ 83.009cc8	:	     40136 │ ff4fff51002f00040000100000000870 │ Picture Essence - 1 frame
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Type                                                ║  Plaintext JPEG2000
 ║   Data                                                ║  ff4fff51002f00040000100000000870…8080808080808080808080808080ffd9
 ║   JPEG2000 Header                                     ║  └──────┘ found here
 ║   JPEG2000 Metadata                                   ║  Unable to decode: BoxValidator.__init__() missing 1 required positional argument: 'boxContents'
 ║   Resource [1]                                        ║  SMPTE.ST.0422-2014 - MXF - Mapping JPEG2000 Codestreams into the MXF Generic Container
 ║   Resource [2]                                        ║  SMPTE.ST.0429-4-2006 - DCP - MXF JPEG2000 Application
 ║   Resource [3]                                        ║  SMPTE.ST.0384M-2005 - TV - MXF - Mapping of Uncompressed Pictures into the Generic Container
 ║   Parser                                              ║  picture_essence
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
27 KLV found in MXF
```



### Extract data from KLV 

```
$ python -m mxf_reader -f tests/assets/2D.mxf -x extract_all_klv/
$ python -m mxf_reader -f tests/assets/2D.mxf --filter "Picture Essence" -x extract_only_picture/
```

Output on `extract_only_picture` directory : 

```
file extract_only_picture/*
00016524-060e2b34010201010d01030115010801-PictureEssence1frame.klv.bin:   data
00016524-060e2b34010201010d01030115010801-PictureEssence1frame.value.bin: JPEG 2000 codestream
```

- `value.bin` contains JPEG2000 content.
- `klv.bin` contains raw KLV content (KLV header and structure of data)
- the first part (00016524) of the filename is the offset number in the MXF
- the second part (060e2b34010201010d01030115010801) of the filename is the key id of the KLV
- the thid part (PictureEssence1frame) is the human readable type of content (based on key id)


Output on `extract_all_klv` directory : 

```
file extract_all_klv/*
00000000-060e2b34020501010d01020101020400-PartitionPackHeaderClosedComplete.klv.bin:              Material exchange container format
00000000-060e2b34020501010d01020101020400-PartitionPackHeaderClosedComplete.value.bin:            data
00000140-060e2b34020501010d01020101050100-PrimerPack.klv.bin:                                     data
00000140-060e2b34020501010d01020101050100-PrimerPack.value.bin:                                   data
00001590-060e2b34025301010d01010101012f00-Preface.klv.bin:                                        data
00001590-060e2b34025301010d01010101012f00-Preface.value.bin:                                      data
00001800-060e2b34025301010d01010101013000-Identification.klv.bin:                                 data
00001800-060e2b34025301010d01010101013000-Identification.value.bin:                               data
00002036-060e2b34025301010d01010101011800-ContentStorage.klv.bin:                                 data
00002036-060e2b34025301010d01010101011800-ContentStorage.value.bin:                               data
00002148-060e2b34025301010d01010101012300-EssenceContainerData.klv.bin:                           data
00002148-060e2b34025301010d01010101012300-EssenceContainerData.value.bin:                         data
00002240-060e2b34025301010d01010101013600-MaterialPackage.klv.bin:                                data
00002240-060e2b34025301010d01010101013600-MaterialPackage.value.bin:                              data
00002420-060e2b34025301010d01010101013b00-TimelineTrack.klv.bin:                                  data
00002420-060e2b34025301010d01010101013b00-TimelineTrack.value.bin:                                data
00002552-060e2b34025301010d01010101010f00-Sequence.klv.bin:                                       data
00002552-060e2b34025301010d01010101010f00-Sequence.value.bin:                                     data
00002652-060e2b34025301010d01010101011400-TimecodeComponent.klv.bin:                              data
00002652-060e2b34025301010d01010101011400-TimecodeComponent.value.bin:                            data
00002747-060e2b34025301010d01010101013b00-TimelineTrack.klv.bin:                                  data
00002747-060e2b34025301010d01010101013b00-TimelineTrack.value.bin:                                data
00002877-060e2b34025301010d01010101010f00-Sequence.klv.bin:                                       data
00002877-060e2b34025301010d01010101010f00-Sequence.value.bin:                                     data
00002977-060e2b34025301010d01010101011100-SourceClip.klv.bin:                                     data
00002977-060e2b34025301010d01010101011100-SourceClip.value.bin:                                   data
00003105-060e2b34025301010d01010101013700-SourcePackage.klv.bin:                                  data
00003105-060e2b34025301010d01010101013700-SourcePackage.value.bin:                                data
00003403-060e2b34025301010d01010101013b00-TimelineTrack.klv.bin:                                  data
00003403-060e2b34025301010d01010101013b00-TimelineTrack.value.bin:                                data
00003535-060e2b34025301010d01010101010f00-Sequence.klv.bin:                                       data
00003535-060e2b34025301010d01010101010f00-Sequence.value.bin:                                     data
00003635-060e2b34025301010d01010101011400-TimecodeComponent.klv.bin:                              data
00003635-060e2b34025301010d01010101011400-TimecodeComponent.value.bin:                            data
00003730-060e2b34025301010d01010101013b00-TimelineTrack.klv.bin:                                  data
00003730-060e2b34025301010d01010101013b00-TimelineTrack.value.bin:                                data
00003860-060e2b34025301010d01010101010f00-Sequence.klv.bin:                                       data
00003860-060e2b34025301010d01010101010f00-Sequence.value.bin:                                     data
00003960-060e2b34025301010d01010101011100-SourceClip.klv.bin:                                     data
00003960-060e2b34025301010d01010101011100-SourceClip.value.bin:                                   data
00004088-060e2b34025301010d01010101012900-RGBAEssenceDescriptor.klv.bin:                          data
00004088-060e2b34025301010d01010101012900-RGBAEssenceDescriptor.value.bin:                        data
00004297-060e2b34025301010d01010101015a00-JPEG2000PictureSubDescriptor.klv.bin:                   data
00004297-060e2b34025301010d01010101015a00-JPEG2000PictureSubDescriptor.value.bin:                 data
00004498-060e2b34010101020301021001000000-KLVFillitemSMPTE.klv.bin:                               data
00004498-060e2b34010101020301021001000000-KLVFillitemSMPTE.value.bin:                             data
00016384-060e2b34020501010d01020101030400-PartitionPackBodyClosedComplete.klv.bin:                data
00016384-060e2b34020501010d01020101030400-PartitionPackBodyClosedComplete.value.bin:              data
00016524-060e2b34010201010d01030115010801-PictureEssence1frame.klv.bin:                           data
00016524-060e2b34010201010d01030115010801-PictureEssence1frame.value.bin:                         JPEG 2000 codestream
00056680-060e2b34020501010d01020101040400-PartitionPackFooterClosedComplete.klv.bin:              data
00056680-060e2b34020501010d01020101040400-PartitionPackFooterClosedComplete.value.bin:            data
00056820-060e2b34025301010d01020101100100-IndexTableSegment2bytesLocalTags2bytesLength.klv.bin:   data
00056820-060e2b34025301010d01020101100100-IndexTableSegment2bytesLocalTags2bytesLength.value.bin: data
```


## Find KLV in broken MXF 

```
$ python -m mxf_reader --fuzzy -f tests/assets/broken.mxf

tests/assets/broken.mxf not a valid MXF
fuzzy mode...
?? 2 060e2b34.04010103.0d010301.027f0100 06
?? 18 060e2b34.04010107.0d010301.020c0100 06
++ 34 060e2b34.02050101.0d010201.01050100 83
++ 1484 060e2b34.02530101.0d010101.01012f00 83
++ 1694 060e2b34.02530101.0d010101.01013000 83
++ 1930 060e2b34.02530101.0d010101.01011800 83
++ 2042 060e2b34.02530101.0d010101.01012300 83
++ 2134 060e2b34.02530101.0d010101.01013600 83
++ 2314 060e2b34.02530101.0d010101.01013b00 83
++ 2446 060e2b34.02530101.0d010101.01010f00 83
++ 2546 060e2b34.02530101.0d010101.01011400 83
++ 2641 060e2b34.02530101.0d010101.01013b00 83
++ 2771 060e2b34.02530101.0d010101.01010f00 83
++ 2871 060e2b34.02530101.0d010101.01011100 83
++ 2999 060e2b34.02530101.0d010101.01013700 83
++ 3297 060e2b34.02530101.0d010101.01013b00 83
++ 3429 060e2b34.02530101.0d010101.01010f00 83
++ 3529 060e2b34.02530101.0d010101.01011400 83
++ 3624 060e2b34.02530101.0d010101.01013b00 83
++ 3754 060e2b34.02530101.0d010101.01010f00 83
++ 3854 060e2b34.02530101.0d010101.01011100 83
++ 3982 060e2b34.02530101.0d010101.01012900 83
++ 4191 060e2b34.02530101.0d010101.01015a00 83
++ 4392 060e2b34.01010102.03010210.01000000 83
++ 16278 060e2b34.02050101.0d010201.01030400 83
++ 16418 060e2b34.01020101.0d010301.15010801 83
++ 56574 060e2b34.02050101.0d010201.01040400 83
++ 56714 060e2b34.02530101.0d010201.01100100 83
++ 56865 060e2b34.02050101.0d010201.01110100 83
```


## Decrypt data

An example with an encrypted JPEG2000 content : 

```
$ python -m mxf_reader -f tests/assets/encrypted-key-00000000000000000000000000000000.mxf --filter "Encrypted Essence Container" -vv -k 00000000000000000000000000000000
 ╓────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 ║   Cryptographic Context Link Length                   ║  16
 ║   Cryptographic Context Link                          ║  67bec4fc.40de4996.aac7fa42.a6b0ed5e
 ║   Plaintext Offset Length                             ║  8
 ║   Plaintext Offset                                    ║  0
 ║   Source Key Length                                   ║  16
 ║   Source Key                                          ║  060e2b34.01020101.0d010301.15010801	(Picture Essence - 1 frame)
 ║   Source Length Length                                ║  8
 ║   Source Length                                       ║  40136
 ║   Encrypted Source Value Length                       ║  40176
 ║   Encrypted Source Value                              ║  765a067b36dfd2e89da94a9c6af0902f7d95b3c594116732ed0b2d9b13ac52839c52432ad90a1bba64fd0ac5c604a1c9… - 40176 bytes
 ║   Encrypted Source Value - IV                         ║  765a067b36dfd2e89da94a9c6af0902f
 ║   Encrypted Source Value - CheckValue                 ║  7d95b3c594116732ed0b2d9b13ac5283
 ║   Encrypted Source Value - Encrypted Data             ║  9c52432ad90a1bba64fd0ac5c604a1c9…ddc25f54eedd18f9b0665f68c04462ef - 40144 bytes, 2509 blocks of 16 bytes (valid)
 ║   TrackFile ID Length                                 ║  16
 ║   TrackFile ID                                        ║  89af85f0.4a1545ec.8a769008.829b2029
 ║   Sequence Number Length                              ║  8
 ║   Sequence Number                                     ║  1
 ║   Message Integrity Code (MIC) Length                 ║  20
 ║   Message Integrity Code (MIC)                        ║  5b594d66d09cf6ddfda8f6e691e4291ea7097bc8
 ║
 ║   Crypto: Check Value Plaintext                       ║  GOOD KEY :) (4348554b4348554b4348554b4348554b)
 ║   Crypto: Frame Plaintext                             ║  JPEG2000 header found
 ║
 ║   JPEG2000 Metadata                                   ║  (....)
 ║   Resource [1]                                        ║  SMPTE.ST.0429-6-2006 - DCP - MXF Track File Essence Encryption
 ║   Resource [2]                                        ║  Page 10
 ║   Parser                                              ║  essence_encrypted
 ╙────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

KLV has been decrypted and JPEG2000 has been found in data.


