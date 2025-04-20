#!/usr/bin/env python3

import io
import os
import sys
import re
import json
import math
import argparse
import signal
import time
from contextlib import suppress

# cryptography
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import ( Cipher, algorithms, modes )
from cryptography.hazmat.backends import default_backend

# xml
from lxml import etree

# jpeg2000
try:
    from jpylyzer import boxvalidator as jpylyzer
except:
    print("Unable to load jpylyzer (no jpeg2000 metadatas)")

# for Essence Sound export
import wave


############# temp ################
def cli_terminal_size():
    import subprocess
    rows = 120
    columns = 40
    try:
        (rows, columns) = subprocess.check_output(['stty', 'size']).split()
        rows = int(rows)
        columns = int(columns)
    except:
        pass
    return {
        "rows": rows,
        "columns": columns
    }
def cli_draw_line():
    return '─' * int(math.floor(CLI_TERMINAL_SIZE['columns']) - 25)

CLI_TERMINAL_SIZE = cli_terminal_size()
CLI_DRAW_LINE = cli_draw_line()

############# temp ################



# -----------------------------------------------
#
#                 Cryptographic
#
# -----------------------------------------------

class Cryptographic():

    # CHUKCHUKCHUKCHUK
    SMPTE_CRYPTOGRAPHIC_CHECK_VALUE_PLAINTEXT=b'\x43\x48\x55\x4B\x43\x48\x55\x4B\x43\x48\x55\x4B\x43\x48\x55\x4B'

    @staticmethod
    def decrypt(key:bytes = b'', iv:bytes = b'', checkvalue:bytes = b'', data:bytes = b'', offset:int = 0):
        plaintext = b''
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        # preprend checkvalue
        if checkvalue:
            decryptor.update(checkvalue)
        # add plaintext content
        if offset != 0:
            plaintext += data[0:offset]
        # release the encryption
        while True:
            buffer = data[offset:offset+16]
            if not buffer:
                break
            plaintext += decryptor.update(buffer)
            offset+=16
        # plaintext += decryptor.finalize()
        return plaintext


# -----------------------------------------------
#
#                     Bytes
#                 (or Format ?)
#
# -----------------------------------------------

class Bytes(bytes):

    def default(bytes) -> str:
        return bytes.hex()

    def unknown(bytes):
        return "%s (!)" % Bytes(bytes).default().upper()

    def uuid(bytes) -> str:
        # SMPTE UL - 12-bytes
        if len(bytes) == 12:
            return "{:02x}{:02x}{:02x}{:02x}.{:02x}{:02x}{:02x}{:02x}.{:02x}{:02x}{:02x}{:02x}".format(*bytes)
        # SMPTE UUID - 16-bytes
        elif len(bytes) == 16:
            return "{:02x}{:02x}{:02x}{:02x}.{:02x}{:02x}{:02x}{:02x}.{:02x}{:02x}{:02x}{:02x}.{:02x}{:02x}{:02x}{:02x}".format(*bytes)
        # ...
        else:
            return bytes.hex()

    # TODO: quick fix (see parsing BER in KLV core)
    # I keep this temp but must be removed/rewritted
    # ------------------------------------------------------------------------
    # SMPTE.EG.0377-3-2013 - MXF Engineering Guideline.pdf - Page 11
    # 40h                       ->  short form coded
    # 83.00.00.40               ->  long form coding using 4 bytes overall
    # 87.00.00.00.00.00.00.40   ->  long form coding using 8 bytes overall
    # ------------------------------------------------------------------------
    # using (80 - BER) = number of bytes to be readed after
    # ex:    <81 = the size value is the BER
    # ex:  80-81 = 1 byte after is the size value
    # ex:  80-83 = 3 bytes after are the size value
    # ex:  80-87 = 7 bytes after are the size value
    # ------------------------------------------------------------------------
    def to_int_ber(bytes) -> int:
        shift = 0x00000000
        if len(bytes) > 0:
            if bytes[0] == 131:
                shift = 0x83000000
            elif bytes[0] == 130:
                shift = 0x82000000
        return int.from_bytes(bytes, byteorder='big') ^ shift

    def to_int(bytes) -> int:
        return int.from_bytes(bytes, byteorder='big')

    def to_string(bytes):
        return bytes.decode('utf').replace('\x00', '')

    def batch_ul(bytes):
        number_of_items = Bytes(bytes[0:4]).to_int()
        length = Bytes(bytes[4:8]).to_int()
        data = bytes[8:]
        uls = []
        for i in range(0, number_of_items):
            uls.append(
                str(Bytes(data[ i*length : (i*length)+length ]).uuid())  # force uuid format
            )
        return "%d item(s): %s" % (number_of_items, ', '.join(uls))

    # alias for batch_ul
    def batch_item(bytes):
        return batch_ul(bytes)

    def rgba_layout(bytes):
        # rgba layout has 8 elements (2 bytes for each elements)
        elements = []
        for i in range(0, 16, 2):
            code = bytes[i:i+1]
            depth = bytes[i+1:i+2]
            elements.append(
                "%s - %d bytes" % (RGBA_LAYOUT.get(code.hex()), Bytes(depth).to_int())
            )
        return "%d item(s): %s" % (len(elements), ', '.join(elements))

    def timestamp(bytes):
        year   = Bytes(bytes[0:2]).to_int()
        month  = Bytes(bytes[2:3]).to_int()
        day    = Bytes(bytes[3:4]).to_int()
        hour   = Bytes(bytes[4:5]).to_int()
        minute = Bytes(bytes[5:6]).to_int()
        second = Bytes(bytes[6:7]).to_int()
        msec   = Bytes(bytes[7:8]).to_int()
        return "%04d-%02d-%02d %02d:%02d:%02d.%04d+00:00" % (year, month, day, hour, minute, second, msec)

    def versioning(bytes):
        # major, minor, tertiary, patch and release version
        # release version : 
        #   0 = Unknown version,
        #   1 = Released version,
        #   2 = Development version,
        #   3 = Released version with patches,
        #   4 = Pre-release beta version,
        #   5 = Private version not intended for general release.
        major    = Bytes(bytes[0:2]).to_int()
        minor    = Bytes(bytes[2:4]).to_int()
        tertiary = Bytes(bytes[4:6]).to_int()
        patch    = Bytes(bytes[6:8]).to_int()
        release  = Bytes(bytes[8:10]).to_int()
        return "%s.%s.%s.%s.%s" % (major, minor, tertiary, patch, release)

    def umid(bytes):
        ul = Bytes(bytes[0:12]).uuid()
        length = bytes[12:13].hex()
        if length == '13':
            umid_format = "Basic" # 32-bytes
        elif length == '53':
            umid_format = "Extended" # 64-bytes
        else:
            umid_format = "Unknown"
        instance = bytes[13:16].hex()
        materiel = Bytes(bytes[16:32]).uuid()
        # UL = Universal Label
        # UMID = Unique material ID
        return "UL:{ul}, Length:{length} ({format} UMID Format), Instance:{instance}, Materiel:{materiel}".format(
            ul=ul,
            length=length,
            instance=instance,
            materiel=materiel,
            format=umid_format
        )

    def edit_rate(bytes):
        return "%d/%d" % (
            Bytes(bytes[0:4]).to_int(), 
            Bytes(bytes[4:8]).to_int()
        )

    def aspect_ratio(bytes):
        width = Bytes(bytes[0:4]).to_int()
        height = Bytes(bytes[4:8]).to_int()
        ratio = 0
        if width != 0 and height != 0:
            ratio = (width / height)
        return "%d/%d (%.02f)" % (
            width, height,
            ratio
        )

    def boolean(bytes):
        return bool(Bytes(bytes).to_int())

    def frame_layout(bytes):
        return "%s (%s)" % (
            FRAME_LAYOUT_LIST.get(
                str(Bytes(bytes).to_int()),
                "UNKNOWN"
            ),
            Bytes(bytes).to_int()
        )

    def picture_essence_coding(bytes):
        return "%s (%s)" % (
            PICTURE_ESSENCE_CODING_LIST.get(
                bytes.hex(),
                "Unknown"
            ),
            bytes.hex()
        )

    def resolution_size(bytes):
		# ISO/IEC 15444-1 - JPEG2000 - Annex A.5 Table A-10
        resolutions = {
			0x0000: "Undefined Profile",
			0x0001: "Profile 1",
			0x0002: "Profile 2",
            0x0003: "2K D-Cinema Profile",
            0x0004: "4K D-Cinema Profile",
			0x0005: "2K Scalable D-Cinema Profile",
			0x0006: "4K Scalable D-Cinema Profile",
			0x0007: "Long Term Storage D-Cinema Profile",
			0x0400: "2K IMF Profile",
			0x0500: "4K IMF Profile",
			0x0600: "8K IMF Profile",
        }
        return "%s (%02Xh)" % (
            resolutions.get(Bytes(bytes).to_int()), 
            Bytes(bytes).to_int()
        )

    def picture_component_sizing(bytes):
        number_of_elements = Bytes(bytes[0:4]).to_int()
        length = Bytes(bytes[4:8]).to_int()
        data = bytes[8:]
        elements = []
        for i in range(0, number_of_elements):
            element = data[3*i:(3*i)+3]
            elements.append(
                "{Ssiz : %s (0x%s), XRSiz : %s (0x%s), YRSiz : %s (0x%s)}" % (
                    Bytes(element[0:1]).to_int(),
                    element[0:1].hex(),
                    Bytes(element[1:2]).to_int(),
                    element[1:2].hex(),
                    Bytes(element[2:3]).to_int(),
                    element[2:3].hex(),
                )
            )
        return "%s elements (%s bytes each) => %s" % (
                number_of_elements,
                length,
                ', '.join(elements),
            )

    def uuid_ul(bytes):
        return "%s\t(%s)" % (
            Bytes(bytes).uuid(),
            UNIVERSAL_LABELS.get(
                bytes.hex().lower(),
                {"name": "Unknown"}
            ).get('name'),
        )

    def entry_array(bytes):
        number_of_entries = Bytes(bytes[0:4]).to_int()
        length = Bytes(bytes[4:8]).to_int()
        return "%d entries (%d bytes each)" % (number_of_entries, length)

    def delta_entry_array(bytes):
        # SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 104
        # for number_of_entries:
        #   PosTableIndex = 8:9    (1B)  \
        #   Slice         = 9:10   (1B)   |---- length (6B)
        #   Element Delta = 10:14  (4B)  /
        return Bytes.entry_array(bytes)

    def index_entry_array(bytes):
        # SMPTE.ST.0377-1-2011 - MXF - File Format Specification - page 105
        # for number_of_entries:
        #   Temporal Offset  : 1B       \
        #   Key-Frame Offset : 1B        |
        #   Flags            : 1B        |____ length (>23B)
        #   Stream Offset    : 8B        |
        #   SliceOffset      : 4B * NSL  |
        #   PosTable         : 8B * NPE /
        return Bytes.entry_array(bytes)

    def split(bytes, maximum:int = 50):
        length = int(len(bytes)/maximum)+1
        for i in range(length):
            offset = maximum * i
            yield bytes[offset:offset + maximum].hex()

    """
    Default coding style for all components. 
    Use this value only if static for all pictures in the Essence Container.

    The data format is as defined in ISO/IEC 15444-1, Annex A.6.1 
    and comprises the sequence of 

        Scod (1 byte per table A-12), 
        SGcod (4 bytes per Table A.12) and 
        Spcod (5 bytes plus 0 or more precinct size bytes per Table A.12)

    JPEG2000 - ISO/IEC 15444-1:2019 (INCITS+ISO+IEC+15444-1-2000.pdf) :
	    Annexe A.6.1 - Coding Style Default (COD)
        Table A-12 (page 42)
    """
    # TODO: do better :)
    def coding_style(bytes):
        buffer = io.BytesIO(bytes)

        elements = []

        # Scod
        elements.append("Scod:0x%s" % buffer.read(1).hex())

        # SGcod
        elements.append("SGcod-ProgressionOrder:0x%s" % buffer.read(1).hex())
        elements.append("SGcod-NumberLayers:0x%s" % buffer.read(2).hex())
        elements.append("SGcod-MultipleComponentTransformation:0x%s" % buffer.read(1).hex())

        # SPcod
        elements.append("SPcod-NumberOfDecompositionLevels:0x%s" % buffer.read(1).hex())
        elements.append("SPcod-CodeBlock-Width:0x%s" % buffer.read(1).hex())
        elements.append("SPcod-CodeBlock-Height:0x%s" % buffer.read(1).hex())
        elements.append("SPcod-CodeBlock-Style:0x%s" % buffer.read(1).hex())
        waveletTransformation = buffer.read(1)
        waveletTransformations = {
            b'\x00' : 'Irreversible',
            b'\x01' : 'Reversible'
        }
        elements.append("SPcod-WaveletTransformation:0x%s (%s)" % (waveletTransformation.hex(), waveletTransformations.get(waveletTransformation)))
        elements.append("SPcod-PrecinctSizeSubband:0x%s" % buffer.read(1).hex())

        element = []
        while True:
            data = buffer.read(1)
            if not data:
                break
            element.append("0x%s" % data.hex())
        elements.append("SPcod-PrecinctSizeResolutionsLevels: %d elements => %s" % (len(element), ', '.join(element)))

        return(', '.join(elements))

    """
	The data format is as defined in ISO/IEC 15444-1, Annex A.6.4 
		and comprises the sequence of 
			Sqcd (1 byte per Table A.27) 
			followed by one or more Sqcd bytes 
			(for the ith subband in the defined order per Table A.27).

    JPEG2000 - ISO/IEC 15444-1:2019 (INCITS+ISO+IEC+15444-1-2000.pdf) :
	    Annexe A.6.4 - Quantization default (QCD)
    """
    def quantization(bytes):
        buffer = io.BytesIO(bytes)
        elements = []
        elements.append("Sqcd-all:0x%s" % buffer.read(1).hex())
        while True:
			# Quantization: 16 bits
			#  5 bits = mantissa
			# 11 bits = exponent
            data = buffer.read(2)
            if not data:
                break
            elements.append("Sqcd[%d]:0x%s" % (len(elements), data.hex()))
        return(', '.join(elements))
        

# -----------------------------------------------
#
#                      KLV
#
# -----------------------------------------------

class KLV(object):
    offset : int = 0
    uuid : bytes = Bytes(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    size : int = 0
    data : bytes = Bytes()

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __repr__(self):
        return("%d, %s, %d, %s" % (
            self.offset,
            self.uuid.uuid(),
            self.size,
            self.data[0:16].hex()
            )
        )


# -----------------------------------------------
#
#                      MXF
#
# -----------------------------------------------

class MXF(object):

    handler:int = None
    filename:str = None
    size:int = 0
    number_of_klv:int = 0

    def __init__(self):
        self.handler = None
        self.filename = None
        self.size = 0

    def open(self, filename: str = None) -> bool:

        # TODO: quick & dirty stdin stream
        # TODO: I don't like it, it's a stupid workaround
        if filename == "-":
            filename = "/tmp/.mxfreader.stream.bin"
            self.stream = open(filename, "wb")  # open buffer file on write-mode
            self._stream = open(0, "rb")  # open stdin on read-mode
            self.stream.write(self._stream.read(2048))  # push stdin into file
            self.stream.flush()

        if os.path.isfile(filename) and os.path.exists(filename):
            self.handler = open(filename, "rb")
            self.filename = filename
            self.size = self.get_size()

            # TODO quick & dirty stdin stream
            if hasattr(self, "stream"):
                self.size = -1

            self.is_mxf = self.is_mxf()
            self.handler.seek(0)
            return True
        return False

    def get_size(self):
        self.handler.seek(0, os.SEEK_END)
        return self.handler.tell()

    def is_mxf(self):
        self.handler.seek(0)
        if self.handler.read(4) == b'\x06\x0e\x2b\x34':
            return True
        return False

    def parse(self) -> KLV:
        while True:

            klv = KLV()

            klv.offset = self.handler.tell()
            klv.key = self.handler.read(16)
            klv.ber = self.handler.read(1)

            """
                TODO: rewrite this with variable BER for long (81-87) and short
                see js-mxf
            """
            # variable BER
            if klv.ber == b'\x87':
                klv.length = self.handler.read(7)
            elif klv.ber == b'\x86':
                klv.length = self.handler.read(6)
            elif klv.ber == b'\x85':
                klv.length = self.handler.read(5)
            elif klv.ber == b'\x84':
                klv.length = self.handler.read(4)
            elif klv.ber == b'\x83':
                klv.length = self.handler.read(3)
            elif klv.ber == b'\x82':
                klv.length = self.handler.read(2)
            elif klv.ber == b'\x81':
                klv.length = self.handler.read(1)
            else:
                klv.length = klv.ber

            klv.uuid = Bytes(klv.key)
            klv.size = Bytes(klv.length).to_int()
            klv.data = Bytes(self.handler.read(klv.size))
            klv.name = None

            # TODO : quick&dirty stdin stream
            if hasattr(self, "stream"):
                self.stream.write(self._stream.read(klv.size + 1024 * 100))

            # break if all bytes has been readed
            if self.size != -1 and self.handler.tell() >= self.size:
                break
            if klv.size == 0:
                break

            self.klv = klv  # save current klv
            self.number_of_klv += 1

            yield klv


    # In case if MXF has been splitted or wrongly generated
    # TODO: merge with fuzzy_klv
    def seek_first_klv(self):
        while True:
            buffer = mxf.handler.read(4)
            if buffer == b'\x06\x0e\x2b\x34':
                mxf.handler.seek(mxf.handler.tell() - 4)
                return True
            if not buffer:
                return False
            self.handler.seek(self.handler.tell() - 3)

    def fuzzy_klv(self):
        while True:
            buffer = self.handler.read(4)
            if buffer == b'\x06\x0e\x2b\x34':
                yield self.handler.tell() - 4
            if self.handler.tell() >= self.size:
                return False
            self.handler.seek(self.handler.tell() - 3)

    def __del__(self):
        if hasattr(self, "stream"):
            print("saved into %s" % self.filename)


# -----------------------------------------------
#
#                     SMPTE
#
# -----------------------------------------------

class SMPTE(object):

    def __init__(self):
        self.load_database()

    def load_database(self):
        database_file = "{path}/database.json".format(path=os.path.dirname(__file__))
        with open(database_file, "r") as handler:
            buffer = json.loads(handler.read())
        self.universal_labels = buffer.get("UniversalLabels")
        self.frame_layout = buffer.get("FrameLayout")
        self.partition_status = buffer.get("PartitionStatus")
        self.picture_essence_coding = buffer.get("PictureEssenceCoding")
        self.rgba_layout = buffer.get("RGBALayout")

    # we can break when it matched, but we can lose a better matching
    # TODO : this is too heavy for CPU. If UL DB grows, it slows down...
    # TODO : find a new way to have a speed matching
    def match_uuid(self, uuid_hex_format: str = None) -> dict:

        # -------------------------------------
        # -- speedy gonzales to find UL info --
        # -------------------------------------

        if value := self.universal_labels.get(uuid_hex_format.lower()):
            return value

        # --------------------------
        # ---- heurestic method ----
        # --------------------------

        matched_values = {}
        # find all matched uuid on database and ordered by number of dots (matches any character)
        # if we have many dots, uuid in database is wider and it least significant too.
        for uuid, values in self.universal_labels.items():
            if re.match(uuid, uuid_hex_format):
                matched_values[uuid.count('.')] = values
        # the most significant to the least significant
        ptr = iter(dict(sorted(matched_values.items())))
        # get the first - most significant - the one with the fewest dots)
        value = matched_values.get(
            next(ptr, 0),
            {}  # default
        )
        return value

    def get_klv_config(self, klv: KLV = None):
        config  = self.match_uuid(klv.uuid.hex())
        klv.name = config.get('name', "(Unknown Key)")
        parser = config.get('parser', 'default')
        klv.resource = config.get('resource', 'default')
        klv.parser = getattr(Parser, parser, Parser.default)
        klv.extract = getattr(Extract, parser, Extract.default)
        klv.display = getattr(Display, parser, Display.default)
        return klv



# -----------------------------------------------
#
#                   Extract
#
# -----------------------------------------------

class Extract():

    @staticmethod
    def default(klv, **kwargs):
        Extract.extract(
            klv = klv,
            path = kwargs.get('path'),
            extension = "value.bin"
        )

    @staticmethod
    def essence_encrypted(klv, **kwargs):

        # Extract raw data
        Extract.extract(
            klv = klv,
            data = klv.data,
            path = kwargs.get('path'),
            extension = "value.bin"
        )
        # IV
        Extract.extract(
            klv = klv,
            data = klv.metadata.IV,
            path = kwargs.get('path'),
            extension = "value.iv.bin"
        )
        # CheckValue
        Extract.extract(
            klv = klv,
            data = klv.metadata.EncryptedCheckValue,
            path = kwargs.get('path'),
            extension = "value.encryptedcheckvalue.bin"
        )
        # Encrypted Frame
        Extract.extract(
            klv = klv,
            data = klv.metadata.EncryptedData,
            path = kwargs.get('path'),
            extension = "value.encryptedframe.bin"
        )
        # Plaintext Frame
        if hasattr(klv.metadata, 'SourceData'):
            Extract.extract(
                klv = klv,
                data = klv.metadata.SourceData,
                path = kwargs.get('path'),
                extension = "j2c"
            )
        return True

    @staticmethod
    def extract(klv, path: str = '/tmp/', data: bytes = None, extension: str = "bin") -> int:
        if data:
            buffer = data
        else:
            buffer = klv.data
        filename = Extract.get_extract_filename(klv)
        if not os.path.exists(path):
            os.mkdir(path)
        with open("%s/%s.%s" % (path, filename, extension), "wb") as handler:
            return handler.write(buffer)
        return -1

    @staticmethod
    def get_extract_filename(klv) -> str:
        # create empty KLV if missing
        if not klv:
            klv = KLV()
        # clear the name
        matches = re.findall("([A-Za-z0-9]+)", getattr(klv, 'name', 'unknown'))
        name = ''.join(matches)
        # construct filename
        return "{offset:08d}-{uuid}-{name}".format(
            offset = klv.offset,
            uuid = klv.uuid.hex(),
            name = name,
        )

    @staticmethod
    def wave_frame_wrapped_essence(klv, **kwargs):

        # TEMP: TODO : construct Header Wav Uncompressed PCM - 32bits - 48khz
        # extract to wav pcm
        wav = KLV()

        # Create RIFF/WAV header
        data = io.BytesIO()
        with wave.open(data, "wb") as file:
            file.setnchannels(2)      # 2 channels
            file.setsampwidth(4)      # bit-depth (4 bytes : 32 bits)
            file.setframerate(48000)  # sampling-rate (48kHz)
        data.seek(0)
        wav.data = data.read()  # save RIFF/WAV header

        # 1 channel - 48kHz - 32 bits
        # wav.data = b"\x52\x49\x46\x46\x94\x12\x01\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x02\x00\x80\xBB\x00\x00\x00\xDC\x05\x00\x08\x00\x20\x00\x64\x61\x74\x61\x70\x12\x01\x00"

        # 6 channels - 44100 hz - 32 bits
        # wav.data = b"\x52\x49\x46\x46\x9C\x22\x2F\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x28\x00\x00\x00\xFE\xFF\x06\x00\x44\xAC\x00\x00\x30\x13\x08\x00\x0C\x00\x10\x00\x16\x00\x10\x00\x3F\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xAA\x00\x38\x9B\x71\x63\x75\x65\x20\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x61\x74\x61\x24\x22\x2F\x00"

        # 6 channels - 48000 hz - 32 bits
        # wav.data = b"\x52\x49\x46\x46\x9C\x22\x2F\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x28\x00\x00\x00\xFE\xFF\x06\x00\x80\xBB\x00\x00\x30\x13\x08\x00\x0C\x00\x10\x00\x16\x00\x10\x00\x3F\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xAA\x00\x38\x9B\x71\x63\x75\x65\x20\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x61\x74\x61\x24\x22\x2F\x00"

        # 8 channels - 48kHz - 32 bits
        # wav.data = b"\x52\x49\x46\x46\xE0\x7F\x8D\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x28\x00\x00\x00\xFE\xFF\x08\x00\x80\xBB\x00\x00\x00\x94\x11\x00\x18\x00\x18\x00\x16\x00\x18\x00\x3F\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xAA\x00\x38\x9B\x71\x63\x75\x65\x20\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x61\x74\x61\x68\x7F\x8D\x00"

        # 8 channels - 44100 hz - 32 bits                                                      channels -------vv      vvvvvv------------ bitrate
        #wav.data = b"\x52\x49\x46\x46\xE0\x7F\x8D\x00\x57\x41\x56\x45\x66\x6D\x74\x20\x28\x00\x00\x00\xFE\xFF\x08\x00\x44\xAC\x00\x00\x00\x94\x11\x00\x18\x00\x18\x00\x16\x00\x18\x00\x3F\x00\x00\x00\x01\x00\x00\x00\x00\x00\x10\x00\x80\x00\x00\xAA\x00\x38\x9B\x71\x63\x75\x65\x20\x34\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x64\x61\x74\x61\x68\x7F\x8D\x00"

        # Create a RIFF/WAV output
        wav.data += klv.data
        wav.name = klv.name
        wav.uuid = klv.uuid
        wav.offset = klv.offset
        Extract.extract(
            klv = wav,
            path = kwargs.get('path'),
            extension = "value.wav"
        )

        # Extract a Raw RIFF/WAV (without headers)
        Extract.extract(
            klv = klv,
            path = kwargs.get('path'),
            extension = "value.bin"
        )


# -----------------------------------------------
#
#                   Display
#
# -----------------------------------------------

class Display():

    @staticmethod
    def default(klv, **kwargs):
        return { "Data": "%s…%s" % (
                klv.data[0:16].hex(),
                klv.data[-16:].hex()
            )
        }

    @staticmethod
    def klv(klv, **kwargs):
        display = {}
        for item in klv.metadata.Items:
            if cli.args.verbose > 1:  # TODO : crappy :-/
                display["%s - %s" % (
                    item.Key.hex().upper(),
                    item.Name
                )] = item.Formatting
            else:
                display[item.Name] = item.Formatting
        return display

    @staticmethod
    def partition_pack(klv, **kwargs):
        return {
            # "MXF Partition Status" : PARTITION_STATUS_LIST.get(ul[14], "Unknown (%d)" % ul[14]),
            "Major Version"        : klv.metadata.MajorVersion,
            "Minor Version"        : klv.metadata.MinorVersion,
            "KAGSize"              : klv.metadata.KAGSize,
            "ThisPartition"        : klv.metadata.ThisPartition,
            "PreviousPartition"    : klv.metadata.PreviousPartition,
            "FooterPartition"      : klv.metadata.FooterPartition,
            "HeaderByteCount"      : klv.metadata.HeaderByteCount,
            "IndexByteCount"       : klv.metadata.IndexByteCount,
            "IndexSID"             : klv.metadata.IndexSID,
            "BodyOffset"           : klv.metadata.BodyOffset,
            "BodySID"              : klv.metadata.BodySID,
            "Operational Pattern"  : Bytes(klv.metadata.OperationalPattern).uuid_ul(),
            "EssenceContainers"    : klv.metadata.EssenceContainers.batch_ul()
        }

    @staticmethod
    def primer_pack(klv, **kwargs):
        display = dict()
        for item in klv.metadata.Items:
            display[item.LocalTag.hex().upper()] = "%s - %s - %s" % (item.AUID.uuid(), item.Info, item.UL)
        return display

    @staticmethod
    def fill_item(klv, **kwargs):
        return { 
            "Data": "%s…%s" % (
                klv.data[0:16].hex(),
                klv.data[-16:].hex()
            )
        }

    @staticmethod
    def essence_encrypted(klv, **kwargs):
        display = {
            "Cryptographic Context Link Length": klv.metadata.CryptographicContextLinkLength,
            "Cryptographic Context Link": str(klv.metadata.CryptographicContextLink),
            "Plaintext Offset Length": klv.metadata.PlaintextOffsetLength,
            "Plaintext Offset": klv.metadata.PlaintextOffset,
            "Source Key Length": klv.metadata.SourceKeyLength,
            "Source Key": "%s" % klv.metadata.SourceKey.uuid_ul(),
            "Source Length Length": klv.metadata.SourceLengthLength,
            "Source Length": klv.metadata.SourceLength,
            "Encrypted Source Value Length": klv.metadata.EncryptedSourceValueLength,
            "Encrypted Source Value" : "%s… - %d bytes" % (
                klv.metadata.EncryptedSourceValue[0:48].hex(),
                len(klv.metadata.EncryptedSourceValue),
            ),
            "Encrypted Source Value - IV": klv.metadata.IV.hex(),
            "Encrypted Source Value - CheckValue": klv.metadata.EncryptedCheckValue.hex(),
            "Encrypted Source Value - Plaintext Data": None,  # prepare this slot if PlaintextData exists
            "Encrypted Source Value - Encrypted Data": "%s…%s - %d bytes, %d blocks of 16 bytes (%s)" % (
                klv.metadata.EncryptedData[0:16].hex(),
                klv.metadata.EncryptedData[-16:].hex(),
                len(klv.metadata.EncryptedData),
                len(klv.metadata.EncryptedData)/16,
                "valid" if len(klv.metadata.EncryptedData)%16 == 0 else "invalid",  # detect if block split is ok
            ),
            "Encrypted Source Value - Encrypted Data - JPEG2000 Header": None,  # prepare this slot for notation (see below)
            "TrackFile ID Length": klv.metadata.TrackFileIDLength,
            "TrackFile ID": klv.metadata.TrackFileID.uuid(),
            "Sequence Number Length": klv.metadata.SequenceNumberLength,
            "Sequence Number": klv.metadata.SequenceNumber,
            "Message Integrity Code (MIC) Length": klv.metadata.MessageIntegrityCodeLength,
            "Message Integrity Code (MIC)": klv.metadata.MessageIntegrityCode.hex()
        }

        if klv.metadata.PlaintextOffset:
            display["Encrypted Source Value - Plaintext Data"] = "%s (%d bytes)" % (
                klv.metadata.PlaintextData.hex(),
                klv.metadata.PlaintextOffset
            )

        # notation for Data
        if klv.metadata.EncryptedData[0:4].hex() == "ff4fff51":
            display.update({"Encrypted Source Value - Encrypted Data - JPEG2000 Header": "\033[34m└──────┘ found here\033[0m"})

        #
        #  TODO : refactoring needed
        #
        if hasattr(klv.metadata, 'EncryptionKeyIsGood'):

            # Check if key is good
            if klv.metadata.EncryptionKeyIsGood is True:
                display["Crypto: Check Value Plaintext"] = "\033[32mGOOD KEY :)\033[0m"
            else:
                display["Crypto: Check Value Plaintext"] = "\033[31mWRONG KEY :(\033[0m"
            display["Crypto: Check Value Plaintext"] += " (%s)" % klv.metadata.PlaintextCheckValue.hex()

            # Check if header is JPEG2000
            if (klv.metadata.SourceDataHeader[0:4].hex() == "ff4fff51"):
                display["Crypto: Frame Plaintext"] = "\033[32mJPEG2000 header found\033[0m"

                if klv.metadata.PlaintextOffset != 0 and not klv.metadata.EncryptionKeyIsGood:
                    display["Crypto: Frame Plaintext"] += " - Key is invalid but header is here because PlaintextOffset"

                # get medatatas 
                if klv.metadata.EncryptionKeyIsGood is True:
                    try:
                        # Only Header or Full Data
                        if hasattr(klv.metadata, 'SourceData'):
                            display.update({'JPEG2000 Metadata' : 'Full'})
                            data = klv.metadata.SourceData
                        else:
                            display.update({'JPEG2000 Metadata' : 'From header only (use extract to get full metadata)'})
                            data = klv.metadata.SourceDataHeader

                        for index, metadata in enumerate(Display.j2c_metadatas(data)):
                            display.update({"JPEG2000 Metadata (%d)" % index : metadata})

                    except Exception as error:
                        display.update({"JPEG2000 Metadata": "Unable to decode: %s" % error})

            else:
                display["Crypto: Frame Plaintext"] = "\033[31mJPEG2000 header NOT found\033[0m"

        return(display)

    @staticmethod
    def random_index_pack(klv, **kwargs):
        display = dict()
        for index, item in enumerate(klv.metadata.Items):
            display["Partition #%s" % index] = "BodySID : %s \t - \t ByteOffset : %12s bytes" % (
                item.BodySID.to_int(),
                item.ByteOffset.to_int()
            )
        display["Length"] = "%s bytes" % klv.metadata.Length.to_int()
        return display

    @staticmethod
    def picture_essence(klv, **kwargs):
        display = {
            "Type": klv.metadata.Type,
            "Data": "%s…%s" % (
                klv.data[0:16].hex(),
                klv.data[-16:].hex()
            )
        }
        # JPEG2000 Header
        if klv.data[0:4].hex() == "ff4fff51":
            display.update({"JPEG2000 Header": "\033[34m└──────┘ found here\033[0m"})

            # get medatatas 
            try:
                for index, metadata in enumerate(Display.j2c_metadatas(klv.data)):
                    display.update({"JPEG2000 Metadata (%d)" % index : metadata})
            except Exception as error:
                display.update({"JPEG2000 Metadata": "Unable to decode: %s" % error})

        return display

    """
        TODO: should be in Parser() ?
    """
    @staticmethod
    def j2c_metadatas(data):
        def walk(elements):
            for property in elements:
                if property.tag and property.text is None:
                    yield "{tag:>36s}".format(tag=property.tag.title())
                    yield from walk(property)
                if property.tag and property.text:
                    yield "{tag:>36s} = {text}".format(tag=property.tag, text=property.text)
        results = jpylyzer.BoxValidator("contiguousCodestreamBox", data).validate()
        return walk(results.characteristics)

    @staticmethod
    def timedtext_essence(klv, **kwargs):
        display = {
            "Type" : klv.metadata.Type,
            "Preview" : "%s…" % klv.data[0:64],
            "Number Of Characters" : "%s characters" % len(klv.data),
            "Number Of Subtitles" : "%s subtitles" % len(klv.metadata.Subtitles),
        }
        # Show all subtitles
        if len(klv.metadata.Subtitles) > 0:
            for index, subtitle in enumerate(klv.metadata.Subtitles):
                display.update({"Subtitles (%d)" % index : "« %s »" % subtitle })
        return display

    @staticmethod
    def wave_frame_wrapped_essence(klv, **kwargs):
        return {
            "Data": "%s…%s" % (
                klv.data[0:16].hex(),
                klv.data[-16:].hex()
            ),
            "Length" : "%s bytes" % len(klv.data)
        }

    @staticmethod
    def immersive_audio_essence(klv, **kwargs):
        return {
            "Data": "%s…%s" % (
                klv.data[0:16].hex(),
                klv.data[-16:].hex()
            ),
            "Length" : "%s bytes" % len(klv.data),

			"PreambleTag"    : klv.metadata.PreambleTag.hex(),
            "PreambleLength" : "%d bytes" % Bytes(klv.metadata.PreambleLength).to_int(),
			"PreambleValue"  : "%s(...)" % klv.metadata.PreambleValue[0:32].hex(),

            "IAFrameTag"     : klv.metadata.IAFrameTag.hex(),
            "IAFrameLength"  : "%d bytes" % Bytes(klv.metadata.IAFrameLength).to_int(),
			"IAFrameValue"   : "%s(...)" % klv.metadata.IAFrameValue[0:32].hex(),

            "IAFrameElementID"   : "%s (%s)" % (klv.metadata.IAFrameElementID.hex(), klv.metadata.IAFrameElementIDName),
            "IAFrameElementSize" : klv.metadata.IAFrameElementSize,
        }

# -----------------------------------------------
#
#                     Parser
#
# -----------------------------------------------

class Parser():

    @staticmethod
    def default(klv, **kwargs):
        buffer = type('object', (), {})() 
        return buffer

    @staticmethod
    def klv(klv, **kwargs):

        h = io.BytesIO(klv.data)
        buffer = type('object', (), {})() 
        
        buffer.Items = list()
        while True:
            entry = type('object', (), {})()
            entry.Key = Bytes(h.read(2))
            if not entry.Key:
                break
            LocalTag = LOCAL_TAGS_LIST.get(entry.Key.hex().upper(), {})
            entry.Length = Bytes(h.read(2)).to_int()
            entry.Value = Bytes(h.read(entry.Length))
            entry.Name = LocalTag.get('name', 'Unknown')
            entry.Format = LocalTag.get('format', '')
            entry.Formatter = getattr(Bytes, entry.Format, Bytes.default)
            entry.Formatting = entry.Formatter(entry.Value)
            buffer.Items.append(entry)

        return buffer

    @staticmethod
    def partition_pack(klv, **kwargs):
        
        h = io.BytesIO(klv.data)
        buffer = type('object', (), {})() 

        buffer.MajorVersion = Bytes(h.read(2)).to_int()
        buffer.MinorVersion = Bytes(h.read(2)).to_int()
        buffer.KAGSize = Bytes(h.read(4)).to_int()
        buffer.ThisPartition = Bytes(h.read(8)).to_int()
        buffer.PreviousPartition = Bytes(h.read(8)).to_int()
        buffer.FooterPartition = Bytes(h.read(8)).to_int()
        buffer.HeaderByteCount = Bytes(h.read(8)).to_int()
        buffer.IndexByteCount = Bytes(h.read(8)).to_int()
        buffer.IndexSID = Bytes(h.read(4)).to_int()
        buffer.BodyOffset = Bytes(h.read(8)).to_int()
        buffer.BodySID = Bytes(h.read(4)).to_int()
        buffer.OperationalPattern = Bytes(h.read(16))
        buffer.EssenceContainers = Bytes(h.read())

        return buffer

    @staticmethod
    def primer_pack(klv, **kwargs):

        h = io.BytesIO(klv.data)
        buffer = type('object', (), {})() 

        buffer.NumberOfItems = Bytes(h.read(4)).to_int()
        buffer.ItemLength = Bytes(h.read(4)).to_int()
        buffer.Items = list()

        for i in range(0, buffer.NumberOfItems):
            entry = type('object', (), {})()
            entry.LocalTag = Bytes(h.read(2))
            entry.AUID = Bytes(h.read(16))
            entry.Info = "Unknown Local Tags"
            if 0x0001 <= entry.LocalTag.to_int() <= 0x00FF:
                entry.Info = "Reserved compatibility AAF"
            if 0x0100 <= entry.LocalTag.to_int() <= 0x7FFF:
                entry.Info = "Statically Local Tags"
            if 0x8000 <= entry.LocalTag.to_int() <= 0xFFFF:
                entry.Info = "Dynamically Local Tags"
            entry.UL = UNIVERSAL_LABELS.get(entry.AUID.hex(), {}).get("name", "")
            buffer.Items.append(entry)

            # TODO : temporary
            UL_DATA = UNIVERSAL_LABELS.get(entry.AUID.hex(), {"name": "**NOT FOUND**", "localtag": entry.LocalTag.hex().upper()})
            LOCAL_TAGS_LIST.update({
                entry.LocalTag.hex().upper(): { 
                    "UL" : entry.AUID,
                    **UL_DATA,
                }
            })

        return buffer

    @staticmethod
    def random_index_pack(klv, **kwargs):
        import time
        h = io.BytesIO(klv.data)
        buffer = type('object', (), {})() 
        buffer.Items = list()
        while h.tell() < klv.size - 4:   # 4 = size of last item (Length)
            item = type('object', (), {})()
            item.BodySID    = Bytes(h.read(4))
            item.ByteOffset = Bytes(h.read(8))
            buffer.Items.append(item)
        buffer.Length = Bytes(h.read(4))
        return buffer

    @staticmethod
    def fill_item(klv, **kwargs):
        buffer = type('object', (), {})() 
        return buffer

    @staticmethod
    def picture_essence(klv, **kwargs):
        buffer = type('object', (), {})() 
        buffer.Type = "Unknown"
        if re.match("ff4fff", klv.data[0:12].hex()):
            buffer.Type = "Plaintext JPEG2000"
        return buffer

    @staticmethod
    def essence_encrypted(klv, **kwargs):

        h = io.BytesIO(klv.data)
        buffer = type('object', (), {})() 

        buffer.CryptographicContextLinkLength = Bytes(h.read(4)).to_int_ber()
        buffer.CryptographicContextLink = Bytes(h.read(16)).uuid()
        buffer.PlaintextOffsetLength = Bytes(h.read(4)).to_int_ber()
        buffer.PlaintextOffset = Bytes(h.read(8)).to_int()
        buffer.SourceKeyLength = Bytes(h.read(4)).to_int_ber() 
        buffer.SourceKey = Bytes(h.read(16))
        buffer.SourceLengthLength = Bytes(h.read(4)).to_int_ber() 
        buffer.SourceLength = Bytes(h.read(8)).to_int()
        buffer.EncryptedSourceValueLength = Bytes(h.read(4)).to_int_ber()
        buffer.EncryptedSourceValue = h.read(buffer.EncryptedSourceValueLength)
        # Cryptographic Segment
        buffer.IV = Bytes(buffer.EncryptedSourceValue[0:16])
        buffer.EncryptedCheckValue = Bytes(buffer.EncryptedSourceValue[16:32])
        if buffer.PlaintextOffset:
            buffer.PlaintextData = buffer.EncryptedSourceValue[32:32+buffer.PlaintextOffset]
            buffer.EncryptedData = buffer.EncryptedSourceValue[32+buffer.PlaintextOffset:]
        else:
            buffer.EncryptedData = buffer.EncryptedSourceValue[32:]
        # Optional
        buffer.TrackFileIDLength = Bytes(h.read(4)).to_int_ber()
        buffer.TrackFileID = Bytes(h.read(16))
        buffer.SequenceNumberLength = Bytes(h.read(4)).to_int_ber()
        buffer.SequenceNumber = Bytes(h.read(8)).to_int()
        buffer.MessageIntegrityCodeLength = Bytes(h.read(4)).to_int_ber()
        buffer.MessageIntegrityCode = Bytes(h.read(20))

        # Decryption
        if kwargs.get('key'):

            # Check Value
            buffer.PlaintextCheckValue = Cryptographic.decrypt(
                key = kwargs.get('key'),
                iv = buffer.IV,
                checkvalue = None, # no need checkvalue yet
                data = buffer.EncryptedCheckValue # force data=checkvalue
            )
            buffer.EncryptionKeyIsGood = (buffer.PlaintextCheckValue == Cryptographic.SMPTE_CRYPTOGRAPHIC_CHECK_VALUE_PLAINTEXT)

            # Header (16-bytes only) 
            if buffer.PlaintextOffset:
                buffer.SourceDataHeader = buffer.PlaintextData
            else:
                buffer.SourceDataHeader = Cryptographic.decrypt(
                    key = kwargs.get('key'),
                    iv = buffer.IV,
                    checkvalue = buffer.EncryptedCheckValue,
                    data = buffer.EncryptedData[0:256],  # 256-bytes - header only
                    offset = buffer.PlaintextOffset
                )

            # Frame (full decryption)
            if kwargs.get("extract"):
                buffer.SourceData = Cryptographic.decrypt(
                    key = kwargs.get('key'),
                    iv = buffer.IV,
                    checkvalue = buffer.EncryptedCheckValue,
                    data = buffer.EncryptedData,
                    offset = 0
                )[0:buffer.SourceLength]
                if buffer.PlaintextOffset:
                    buffer.SourceData = (buffer.PlaintextData + buffer.SourceData)
                # remove padding
                buffer.SourceData = buffer.SourceData[0:buffer.SourceLength]


        return buffer

    @staticmethod
    def timedtext_essence(klv, **kwargs):
        buffer = type('object', (), {})()
        buffer.Type = "Unknown"
        buffer.Subtitles = list()

        # Parsing XML
        try:
            tree = etree.fromstring(
                text = klv.data
            )
            xpath_text = "//*[local-name()='Text']/text()"
            buffer.Subtitles = tree.xpath(xpath_text)
            buffer.Type = "XML"
        except Exception as error:
            buffer.Type = "XML (malformed) : %s" % error

        return buffer

    @staticmethod
    def wave_frame_wrapped_essence(klv, **kwargs):
        h = io.BytesIO(klv.data)  # not used yet
        buffer = type('object', (), {})() 
        buffer.Data = klv.data
        return buffer

    @staticmethod
    def immersive_audio_essence(klv, **kwargs):

        IAFrameElementIDS = {
			8 : "IAFrame: Frame Header",              # 0x08
            16 : "Bed Definition",		              # 0x10
			32 : "Bed Remap",			              # 0x20
			64 : "Object Definition",                 # 0x40
			128 : "Extended Object Zone Definition",  # 0x80
			256 : "Authoring Tool Information",       # 0x100
			257 : "User Defined Data",                # 0x101
			512 : "Audio Data (DLC Encoded)",         # 0x200
			1024 : "Audio Data PCM",                  # 0x400
        }

        buffer = type('object', (), {})() 
        buffer.Type = "Immersive Audio"

        h = io.BytesIO(klv.data)
        buffer.PreambleTag = h.read(1)
        buffer.PreambleLength = h.read(4)
        buffer.PreambleValue = h.read(Bytes(buffer.PreambleLength).to_int())

        buffer.IAFrameTag = h.read(1)
        buffer.IAFrameLength = h.read(4)
        buffer.IAFrameValue = h.read(Bytes(buffer.IAFrameLength).to_int())

        IAFrame = io.BytesIO(buffer.IAFrameValue)
        buffer.IAFrameElementID = IAFrame.read(1)
        buffer.IAFrameElementIDName = IAFrameElementIDS.get(
            Bytes(buffer.IAFrameElementID).to_int(),
            "Unknown"
        )
        buffer.IAFrameElementSize = IAFrame.read(4)

        return buffer


# --------------------------------------------------
#
#                      Main
#
# --------------------------------------------------


if __name__ == "__main__":

    def sigint_handler(signal, frame):
        sys.exit(254)
    signal.signal(signal.SIGINT, sigint_handler)


    cli = argparse.ArgumentParser()
    cli.add_argument('-f', '--filename', action='store', help='<mxf> = mxf filename')
    cli.add_argument('-x', '--extract', action='store', help='<directory> = extract each KLV into files')
    cli.add_argument('-k', '--key', action='store', help='AES Key, ex. --key 00000000000000000000000000000000')
    cli.add_argument('-v', '--verbose', action="count", default=0, help="increase output verbosity")
    cli.add_argument('-n', '--no-resolv', action='store_true', default=False, help="Do not resolv UL (speed)")
    cli.add_argument('--filter', action='store', help='filter by name')
    cli.add_argument('--fuzzy', action='store_true', help='Fuzzy mode only (very slow)')
    cli.add_argument('--limit', action='store', default=-1, help='stop after x klv parsed')
    cli.add_argument('--slow', action='store_true', default=False, help='Slowdown parse to avoid flood loadavg')
    cli.args = cli.parse_args()

    if not cli.args.filename:
        cli.print_help()
        sys.exit(1)

    if cli.args.key and len(cli.args.key) != 32:
        print("Invalid AES key size (%d bytes missing)" % (32-len(cli.args.key)))
        sys.exit(1)
    elif cli.args.key and len(cli.args.key) == 32:
        cli.args.key=bytes.fromhex(cli.args.key)

    mxf = MXF()

    if not mxf.open(cli.args.filename):
        print("Unable to open {filename}".format(filename=cli.args.filename))
        sys.exit(254)

    if not mxf.is_mxf:
        print("{filename} not a valid MXF".format(filename=cli.args.filename))
        if not cli.args.fuzzy:
            print("Finding KLV...")
            if mxf.seek_first_klv():
                print("First KLV found at offset %d" % mxf.handler.tell())
            else:
                print("No KLV found on %d bytes readed" % mxf.handler.tell())
                sys.exit(253)

    # -- prototype : fuzzy mode -------------------------------------------
    """
        TODO: temporary
    """
    if cli.args.fuzzy:
        print("fuzzy mode...")
        mxf.handler.seek(0)
        for offset in mxf.fuzzy_klv():
            mxf.handler.seek(offset)
            ul = mxf.handler.read(16)
            ber = mxf.handler.read(1)
            # add more BER (81-87) + short BER
            if b'\x81' <= ber <= b'\x87':
                print("++", offset, Bytes(ul).uuid(), ber.hex())
                # seek to speedup the parsing
                if ber == b'\x83':
                    length = Bytes(mxf.handler.read(3)).to_int_ber()
                    mxf.handler.seek(mxf.handler.tell() + length)
            else:
                print("??", offset, Bytes(ul).uuid(), ber.hex())
        sys.exit(0)
    # ---------------------------------------------------------------------

    smpte = SMPTE()
    UNIVERSAL_LABELS = smpte.universal_labels;
    LOCAL_TAGS_LIST = {};

    # -- create initial LocalTags with current database --
    # normally, in Primer Pack, we have ALL Localtag and UniversalLabel
    # but in some MXF, Primer Pack doesn't include all Static Local Tag
    # with this, we create an initial Static Local Tag DB before an update in Primer Pack
    for UL in UNIVERSAL_LABELS:
        localtag = UNIVERSAL_LABELS[UL].get("localtag")
        if localtag and localtag != "dynamic" and len(localtag) == 4:
            LOCAL_TAGS_LIST.update({
                localtag.upper(): { 
                    "UL" : UL,
                    **UNIVERSAL_LABELS[UL],
                }
            })

    FRAME_LAYOUT_LIST = smpte.frame_layout
    PARTITION_STATUS_LIST = smpte.partition_status
    PICTURE_ESSENCE_CODING_LIST = smpte.picture_essence_coding
    RGBA_LAYOUT = smpte.rgba_layout

    if cli.args.verbose >= 2:
        print("Filename %s (%d bytes)" % (mxf.filename, mxf.size))
        print("{number} SMPTE Universal Labels loaded".format(number=len(smpte.universal_labels)))
        print("{number} SMPTE Local Tags loaded".format(number=len(LOCAL_TAGS_LIST)))

    # Disabled verbose and extract in no-resolv
    if cli.args.no_resolv:
        if cli.args.verbose or cli.args.extract:
            print("verbose and extract are disabled in no-resolv mode")
        cli.args.verbose = 0
        cli.args.extract = 0

    if cli.args.slow:
        print("Slow mode activated")

    # output header
    print("\033[30m{offset:>12s} │ {uuid:35s} │ {ber:<9s}\t:\t{size:>10s} │ {data:>32s} │ {name}\033[0m".format(
        offset="offset",
        uuid="uuid",
        ber="ber",
        size="data-size",
        data="data",
        name="name",
    ))

    for index, klv in enumerate(mxf.parse()):

        if cli.args.slow:
            time.sleep(0.05)

        if int(cli.args.limit) >= 0 and index >= int(cli.args.limit):
            print("(limit %d klv reached)" % int(cli.args.limit))
            break

        if not cli.args.no_resolv:
            klv = smpte.get_klv_config(klv)
        else:
            klv.name = ""

        # Add filter on output
        if cli.args.filter:
            with suppress(re.error):
                if (not re.search(cli.args.filter, klv.name, re.IGNORECASE) and \
                   not re.search(cli.args.filter, klv.uuid.uuid(), re.IGNORECASE)) and \
                   klv.uuid.hex() != "060e2b34020501010d01020101050100":  # primer pack  (need to load this klv for local tag)  # TODO temp
                    continue

        # TODO : temp
        if cli.args.filter and klv.uuid.hex() == "060e2b34020501010d01020101050100":
            pass
        else:
            print("\033[32m{offset:12d} │ {uuid} │ {ber}.{ber_size:<6s}\t:\t{size:>10d} │ {data:>32s} │ {name}\033[0m".format(
                offset = klv.offset,
                uuid = klv.uuid.uuid(),
                ber = klv.ber.hex(),
                ber_size = klv.length.hex() if 0x80 < Bytes(klv.ber).to_int() <= 0x87 else '\010',  # don't display on short-form-coding
                size = klv.size,
                data = klv.data[0:16].hex(),
                name = klv.name
            ))

        if cli.args.verbose or cli.args.extract:

            # parser
            klv.metadata = klv.parser(
                klv = klv,
                key=cli.args.key,         # for encryption
                extract=cli.args.extract  # for encryption (full decryption)
            )
            
            # display
            formatting = klv.display(
                klv = klv
            )

            # Resource(s)
            for index, resource in enumerate(klv.resource.split(','), 1):
                formatting['Resource [%d]' % index] = resource.strip()

            # add parser name
            if cli.args.verbose >= 2:
                formatting["Parser"] = klv.parser.__name__

            # add splitted data
            if cli.args.verbose >= 3:

                # add key from KLV
                formatting['Data - Key'] = klv.uuid.hex()
                if cli.args.verbose >= 4:
                    # TODO : write parse/display functions
                    formatting['Data - Key - UL Header (2 bytes)'] = klv.uuid[0:2].hex()
                    formatting['Data - Key - UL Designator (6 bytes)'] = klv.uuid[2:8].hex()
                    formatting['Data - Key - Item Designator (8 bytes)'] = klv.uuid[8:].hex()
                    formatting["Data - Key[1] - Object ID"] = klv.uuid[0:1].hex()
                    formatting["Data - Key[2] - UL Size"] = klv.uuid[1:2].hex()
                    formatting["Data - Key[3] - ISO/ORG Identifier"] = klv.uuid[2:3].hex()
                    formatting["Data - Key[4] - SMPTE Identifier"] = klv.uuid[3:4].hex()

                    # Category Type (TODO: rewrite this)
                    formatting["Data - Key[5] - Category Designator"] = klv.uuid[4:5].hex()  # SMPTE-336M - Table 3 – UL Designator
                    if klv.uuid[4:5].hex() == '01': formatting["Data - Key[5] - Category Designator"] += " (Dictionaries)"
                    if klv.uuid[4:5].hex() == '02': formatting["Data - Key[5] - Category Designator"] += " (Groups - Sets & Packs)"

                    # Registry Type  (TODO: rewrite this)
                    formatting["Data - Key[6] - Registry Designator"] = klv.uuid[5:6].hex()
                    if klv.uuid[4:6].hex() == '0101': formatting["Data - Key[6] - Registry Designator"] += " (Metadata Dictonary)"
                    if klv.uuid[4:6].hex() == '0102': formatting["Data - Key[6] - Registry Designator"] += " (Essence Dictonary)"
                    if klv.uuid[4:6].hex() == '0204': formatting["Data - Key[6] - Registry Designator"] += " (Variable Length Pack)"
                    if klv.uuid[4:6].hex() == '0205': formatting["Data - Key[6] - Registry Designator"] += " (Defined Length Pack)"
                    if klv.uuid[4:6].hex() == '0253': formatting["Data - Key[6] - Registry Designator"] += " (Local Sets)"

                    formatting["Data - Key[7] - Structure Designator"] = klv.uuid[6:7].hex() # SMPTE-336M - Table 3 – UL Designator
                    formatting["Data - Key[8] - Version"] = klv.uuid[7:8].hex()
                    for i in range(8, 16):
                        formatting["Data - Key[%d] - Item Designator" % (i+1)] = klv.uuid[i:i+1].hex()

                # add length from KLV
                formatting["Data - Length"] = "%s (%d bytes)" % (klv.length.hex(), Bytes(klv.length).to_int())

                # add value from KLV
                split_size = int(CLI_TERMINAL_SIZE['columns']/5)
                for index, data in enumerate(klv.data.split(maximum=split_size)):
                    formatting["Data - Value [%d]" % index] = data
                    if cli.args.verbose <= 3 and index > 5:
                        formatting["Data - Value [%d]" % index] = "(%d more...)" % ((len(klv.data) / split_size) - 6)
                        break

                # add plaintext data (encrypted layer)
                if cli.args.key:
                    plaintext = b''

                    # full decryption
                    if hasattr(klv.metadata, 'SourceData'):
                        plaintext = Bytes(klv.metadata.SourceData) 

                    # header decryption
                    elif hasattr(klv.metadata, 'SourceDataHeader'):
                        plaintext = Bytes(klv.metadata.SourceDataHeader)

                    for index, data in enumerate(plaintext.split()):
                        formatting["Plaintext Data [%d]" % index] = data
                        if cli.args.verbose <= 3 and index > 5:
                            break

            # TODO : temp : remove primer pack display on filter (temporary solution)
            if cli.args.filter and klv.uuid.hex() == "060e2b34020501010d01020101050100":  # primer pack  (need to load this klv for local tag)
                continue

            # --------- display metadata --------
            print("\t ╓%s" % CLI_DRAW_LINE)
            for key, value in formatting.items():
                if value is not None:
                    print("\t ║   {key:50s}  ║  {value}".format(key=key, value=value))
            print("\t ╙%s" % CLI_DRAW_LINE)

            if cli.args.extract:
                klv.extract(
                    klv = klv,
                    path = cli.args.extract,
                    extension = "value.bin"
                )
                # full klv  # TODO
                filename = Extract.get_extract_filename(klv)
                with open("%s/%s.klv.bin" % (cli.args.extract, filename), "wb") as handler:
                    handler.write(klv.key+klv.ber+klv.length+klv.data)

    if cli.args.verbose >= 2:
        print("{number} KLV found in MXF".format(number=mxf.number_of_klv))


