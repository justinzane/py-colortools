'''
@file images.py
@author Justin Zane Chudgar <justin@justinzane.com>
@license GPLv3
@brief Generic image structures for py-colortools.
@note: Though Lindbloom uses the convention of subpixel subscripted with 'r' to
       indicate whitepoint adjusted values; this module uses 'w' as a postfix
       on variable names. I.e. X_r from Lindbloom becomes xw here.
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
        ''' @note Tested and working. '''
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
                self.data[y][x][0] = xval
                self.data[y][x][1] = yval
                self.data[y][x][2] = zval
        maxval = max(max(max(self.data)))
        minval = min(min(min(self.data)))
        valrange = maxval - minval
        print("xyz MAX: %f, MIN: %f, RANGE: %f" % (maxval, minval, valrange))


    def _xyz2rgb(self):
        ''' @note Tested and working. '''
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
                self.data[y][x][0] = r
                self.data[y][x][1] = g
                self.data[y][x][2] = b
        maxval = max(max(max(self.data)))
        minval = min(min(min(self.data)))
        valrange = maxval - minval
        print("rgb MAX: %f, MIN: %f, RANGE: %f" % (maxval, minval, valrange))


    @classmethod
    def _lab_f (cls, val):
        if (val > colorspaces.LAB_ETA):
            return math.pow(val, 1.0/3.0)
        else:
            return (colorspaces.LAB_LAMBDA * val + colorspaces.LAB_MU)

    def _xyz2lab(self):
        '''
        @note Tested and working.
        '''
        for y in range(self.height):
            for x in range(self.width):
                xw = self.data[y][x][0] / self.colorspace['whitepoint_xyz'][0]
                yw = self.data[y][x][1] / self.colorspace['whitepoint_xyz'][1]
                zw = self.data[y][x][2] / self.colorspace['whitepoint_xyz'][2]
                lval = 116.0 * raw_img._lab_f(yw) - 16.0
                aval = 500.0 * (raw_img._lab_f(xw) - raw_img._lab_f(yw))
                bval = 200.0 * (raw_img._lab_f(yw) - raw_img._lab_f(zw))
                self.data[y][x][0] = lval
                self.data[y][x][1] = aval
                self.data[y][x][2] = bval


    @classmethod
    def _inv_f_lab(cls, val):
        '''@brief Private helper for _lab2xyz; see
        (https://en.wikipedia.org/wiki/Lab_color_space) for info.'''
        if val > (6.0/29.0):
            return math.pow(val, 3.0)
        else:
            return (3.0 *
                    math.pow((6.0 / 29.0), 2.0) *
                    (val - (4.0 / 29.0)))

    def _lab2xyz(self):
        '''
        @brief Convert from CIE Lab to CIE XYZ space; see
        (https://en.wikipedia.org/wiki/Lab_color_space) for info.
        @note Tested and working.
        '''
        for y in range(self.height):
            for x in range(self.width):
                xval = (self.colorspace['whitepoint_xyz'][0] *
                        raw_img._inv_f_lab(((self.data[y][x][0] + 16.0) / 116.0) +
                                            (self.data[y][x][1] / 500.0)))
                yval = (self.colorspace['whitepoint_xyz'][1] *
                        raw_img._inv_f_lab((self.data[y][x][0] +16.0) / 116.0))
                zval = (self.colorspace['whitepoint_xyz'][2] *
                        raw_img._inv_f_lab(((self.data[y][x][0] +16.0) / 116.0) -
                                            (self.data[y][x][2] / 200.0)))
                self.data[y][x][0] = xval
                self.data[y][x][1] = yval
                self.data[y][x][2] = zval
        maxval = max(max(max(self.data)))
        minval = min(min(min(self.data)))
        valrange = maxval - minval
        print("xyz MAX: %f, MIN: %f, RANGE: %f" % (maxval, minval, valrange))


    def _lab2lhc(self):
        ''' @note Tested and working. '''
        for y in range(self.height):
            for x in range(self.width):
                cval = math.sqrt(math.pow(self.data[y][x][1], 2) +
                                 math.pow(self.data[y][x][2], 2))
                hval = math.atan2(self.data[y][x][2], self.data[y][x][1])
                self.data[y][x][1] = hval
                self.data[y][x][2] = cval


    def _lhc2lab(self):
        ''' @brief Converts from CIE LHC space to CIE Lab.
            @note Tested and working. '''
        for y in range(self.height):
            for x in range(self.width):
                aval = self.data[y][x][2] * math.cos(self.data[y][x][1])
                bval = self.data[y][x][2] * math.sin(self.data[y][x][1])
                self.data[y][x][1] = aval
                self.data[y][x][2] = bval

    def _normalize(self):
        for y in range(self.height):
            for x in range(self.width):
                for sp in range(self.channels):
                    if self.data[y][x][sp] > 1.0:
                        self.data[y][x][sp] = 1.0
                    elif self.data[y][x][sp] < 0.0:
                        self.data[y][x][sp] = 0.0

    def do_nothing(self):
        self._rgb2xyz()
        self._xyz2lab()
        self._lab2lhc()
        self._lhc2lab()
        self._lab2xyz()
        self._xyz2rgb()

    def adj_hue_deg(self, adj_deg):
        self._rgb2xyz()
        self._xyz2lab()
        self._lab2lhc()

        adj = math.pi * adj_deg / 180.0
        for y in range(self.height):
            for x in range(self.width):
                self.data[y][x][1] = self.data[y][x][1] + adj

        self._lhc2lab()
        self._lab2xyz()
        self._xyz2rgb()
        self._normalize()
