'''
@file images.py
@author Justin Zane Chudgar <justin@justinzane.com>
@license GPLv3
@brief Generic image structures for py-colortools.
'''

import colorspaces
import ctypes
import math

class raw_img (object):
    """ WRITEME """
    DTYPES = [ctypes.c_uint8, ctypes.c_uint16, float]
    CHANNELS = [1, 3, 4]

    def __init__(self):
        self.width = -1
        self.height = -1
        self.channels = 4
        self.datatype = raw_img.DTYPES[2]
        self.colorspace = colorspaces.sRGB
        self.data = None

    def _convert_dtype(self, new_type):
        if not new_type in raw_img.DTYPES:
            print("Invalid type provided.")
            return
        if new_type == self.datatype:
            print("New type is the same as the old type.")
            return
        self.datatype = new_type
        for y in range(self.height):
            for x in range(self.width):
                for sp in range(self.channels):
                    self.data[y][x][sp] = self.datatype(self.data[y][x][sp])

    def _rgb2xyz(self):
        if not self.datatype == raw_img.DTYPES[2]:
            self.convert_dtype(raw_img.DTYPES[2])
        for y in range(self.height):
            for x in range(self.width):
                xval = (self.data[y][x][0] * self.colorspace['rgb2xyz_m'][0][0] +
                        self.data[y][x][1] * self.colorspace['rgb2xyz_m'][0][1] +
                        self.data[y][x][2] * self.colorspace['rgb2xyz_m'][0][2])
                yval = (self.data[y][x][0] * self.colorspace['rgb2xyz_m'][1][0] +
                        self.data[y][x][1] * self.colorspace['rgb2xyz_m'][1][1] +
                        self.data[y][x][2] * self.colorspace['rgb2xyz_m'][1][2])
                zval = (self.data[y][x][0] * self.colorspace['rgb2xyz_m'][2][0] +
                        self.data[y][x][1] * self.colorspace['rgb2xyz_m'][2][1] +
                        self.data[y][x][2] * self.colorspace['rgb2xyz_m'][2][2])
                if (y == 0 and x == 0):
                    print("RGB: %f, %f, %f\nXYZ: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           xval, yval, zval))
                self.data[y][x][0] = xval
                self.data[y][x][1] = yval
                self.data[y][x][2] = zval


    def _xyz2rgb(self):
        for y in range(self.height):
            for x in range(self.width):
                r = (self.data[y][x][0] * self.colorspace['xyz2rgb_m'][0][0] +
                     self.data[y][x][1] * self.colorspace['xyz2rgb_m'][0][1] +
                     self.data[y][x][2] * self.colorspace['xyz2rgb_m'][0][2])
                g = (self.data[y][x][0] * self.colorspace['xyz2rgb_m'][1][0] +
                     self.data[y][x][1] * self.colorspace['xyz2rgb_m'][1][1] +
                     self.data[y][x][2] * self.colorspace['xyz2rgb_m'][1][2])
                b = (self.data[y][x][0] * self.colorspace['xyz2rgb_m'][2][0] +
                     self.data[y][x][1] * self.colorspace['xyz2rgb_m'][2][1] +
                     self.data[y][x][2] * self.colorspace['xyz2rgb_m'][2][2])
                if (y == 0 and x == 0):
                    print("XYZ: %f, %f, %f\nRGB: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           r, g, b))
                self.data[y][x][0] = r
                self.data[y][x][1] = g
                self.data[y][x][2] = b

    @classmethod
    def _lab_f (cls, val):
        if (val <= colorspaces.LAB_ETA):
            return (colorspaces.LAB_LAMBDA * val + colorspaces.LAB_MU)
        else:
            return math.pow(val, 1.0/3.0)

    def _xyz2lab(self):
        for y in range(self.height):
            for x in range(self.width):
                xw = self.data[y][x][0] / self.colorspace['whitepoint_xyz'][0]
                yw = self.data[y][x][0] / self.colorspace['whitepoint_xyz'][1]
                zw = self.data[y][x][0] / self.colorspace['whitepoint_xyz'][2]
                lval = 116.0 * raw_img._lab_f(yw) - 16.0
                aval = 500.0 * (raw_img._lab_f(xw) - raw_img._lab_f(yw))
                bval = 200.0 * (raw_img._lab_f(yw) - raw_img._lab_f(zw))
                if (y == 0 and x == 0):
                    print("XYZ: %f, %f, %f\nLAB: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           lval, aval, bval))
                self.data[y][x][0] = lval
                self.data[y][x][1] = aval
                self.data[y][x][2] = bval


    def _lab2xyz(self):
        for y in range(self.height):
            for x in range(self.width):
                p = (self.data[y][x][0] + 16.0) / 116.0
                xval = (self.colorspace['whitepoint_xyz'][0] *
                        math.pow((p + self.data[y][x][1] / 500.0), 3))
                yval = (self.colorspace['whitepoint_xyz'][1] *
                        math.pow(p, 3))
                zval = (self.colorspace['whitepoint_xyz'][2] *
                        math.pow((p + self.data[y][x][2] / 200.0), 3))
                if (y == 0 and x == 0):
                    print("LAB: %f, %f, %f\nXYZ: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           xval, yval, zval))
                self.data[y][x][0] = xval
                self.data[y][x][1] = yval
                self.data[y][x][2] = zval

    def _lab2lhc(self):
        for y in range(self.height):
            for x in range(self.width):
                cval = math.sqrt(math.pow(self.data[y][x][1], 2) +
                                 math.pow(self.data[y][x][2], 2))
                if self.data[y][x][1] == 0.0:
                    hval = 0.0
                else:
                    hval = math.atan(self.data[y][x][2] / self.data[y][x][1])
                    if hval < 0.0:
                        hval += 2.0 * math.pi
                    elif hval >= (2.0 * math.pi) :
                        hval += 2.0 * math.pi
                if (y == 0 and x == 0):
                    print("LAB: %f, %f, %f\nLHC: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           self.data[y][x][0], hval, cval))
                self.data[y][x][1] = hval
                self.data[y][x][2] = cval

    def _lhc2lab(self):
        for y in range(self.height):
            for x in range(self.width):
                aval = self.data[y][x][2] * math.cos(self.data[y][x][1])
                bval = self.data[y][x][2] * math.sin(self.data[y][x][1])
                if (y == 0 and x == 0):
                    print("LHC: %f, %f, %f\nLAB: %f, %f, %f\n" %
                          (self.data[y][x][0], self.data[y][x][1], self.data[y][x][2],
                           self.data[y][x][0], aval, bval))
                self.data[y][x][1] = aval
                self.data[y][x][2] = bval

    def adj_hue_deg(self, adj_deg):
        self._rgb2xyz()
        self._xyz2lab()
        self._lab2lhc()

        twopi = 2.0 * math.pi
        adj = adj_deg / twopi
        for y in range(self.height):
            for x in range(self.width):
                self.data[y][x][1] = (self.data[y][x][1] + adj) % twopi

        self._lhc2lab()
        self._lab2xyz()
        self._xyz2rgb()
