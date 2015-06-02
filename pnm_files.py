"""
@author   Justin Zane Chudgar <justin@justinzane.com>
@file     py-colortools.py
@license  GPLv3
@brief    WRITEME
"""

import colorspaces
from images import raw_img
import re

class ppm_file (object):
    MN_RE = re.compile(r'^([^\t\n ]+)')
    PPM_RE = re.compile(r'P3')
    COMMENT_RE = re.compile(r'^#.*')
    DIMENSION_RE = re.compile(r'^([0-9]+)[\t ]+([0-9]+)[\t ]*$')
    MAX_VAL_RE = re.compile(r'^([0-9]+)[\t ]*$')
    DATA_RE = re.compile(r'^(([0-9]+)([\t ]+|$))+')

    def __init__(self):
        self.magic_num = ""
        self.max_val = -1
        self.comments = ""
        self.img = raw_img()
        self.img.channels = 3
        self.img.colorspace = colorspaces.NTSC_RGB
        self.img.datatype = raw_img.DTYPES[2]

    @classmethod
    def _get_magic_number(cls, line):
        match = cls.MN_RE.match(line)
        if not (match == None):
            return match.group(1)
        else:
            return None

    @classmethod
    def _get_comment(cls, line):
        cmt = cls.COMMENT_RE.match(line)
        if cmt == None:
            return None
        else:
            return cmt.group(0)

    @classmethod
    def _get_dimensions(cls, line):
        match = cls.DIMENSION_RE.match(line)
        if match == None:
            return None
        else:
            retval = [int(match.group(1)), int(match.group(2))]
            if ((retval[0] >=0 ) and (retval[1] >= 0)):
                return retval
            else:
                print("Negative image dimensions, bad PPM file!\n")
                return None

    @classmethod
    def _get_max_val(cls, line):
        match = cls.MAX_VAL_RE.match(line)
        if not match == None:
            return int(match.group(1))
        else:
            return None

    def _get_data(self, lines):
        data = []
        for line in lines:
            m = self.DATA_RE.match(line)
            if (m == None):
                print("No well formatted data in line.\n")
            else:
                numstrs = line.split()
                for d in numstrs:
                    data.append(float(d) / 255.0)
        if not (((len(data) % 3) == 0) and
                ((len(data) % self.img.width) == 0) and
                ((len(data) % self.img.height) == 0)):
            print ("Data length: %d not multiple of 3 * width * height, BAD DATA.\n"
                   % (len(data)))
            return

        rows = []
        for r in range(self.img.height):
            pixels = []
            for p in range(self.img.width):
                idx = ((r * self.img.width * 3) +
                       (p * 3))
                pixels.append(data[idx:idx+3])
            rows.append(pixels)
        self.img.data = rows


    def saveimage(self, img_file_name):
        with open(img_file_name, 'w') as fh:
            fh.write("%s\n" % (self.magic_num))
            fh.write("%d %d\n" % (self.img.width, self.img.height))
            fh.write("%d\n" % (self.max_val))
            line = ""
            for y in range(self.img.height):
                for x in range(self.img.width):
                    for sp in range(self.img.channels):
                        line += str(int(0.5 + 255.0 * self.img.data[y][x][sp]))
                        if (sp == (self.img.channels -1)) and (len(line) > 68):
                            line += "\n"
                            fh.write(line)
                            line = ""
                        else:
                            line += " "
            fh.write(line + "\n")
            fh.close()

    def loadimage(self, img_file_name):
        with open(img_file_name, 'r') as img_fh:
            src_lines = img_fh.readlines(-1)
            img_fh.close()

        mn = self._get_magic_number(src_lines[0])
        if (mn == None):
            print("Magic Number not in first line. Bad PPM file.")
            return None
        elif self.PPM_RE.match(mn) == None:
            print("Magic Number: %s not \"P3\"" % (mn))
            return None
        else:
            self.magic_num = mn

        while not ((self.max_val >= 0) and
                   (self.img.width >=0) and
                   (self.img.height >=0)):
            src_lines = src_lines[1:]
            cmt = self._get_comment(src_lines[0])
            if not (cmt == None):
                self.comments.append(cmt + "\n")
            else:
                dims = self._get_dimensions(src_lines[0])
                if not dims == None:
                    self.img.width = dims[0]
                    self.img.height = dims[1]
                else:
                    mv = self._get_max_val(src_lines[0])
                    if not mv == None:
                        self.max_val = int(mv)
        self._get_data(src_lines[1:])
