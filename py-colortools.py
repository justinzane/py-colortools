"""
@author   Justin Zane Chudgar <justin@justinzane.com>
@file     py-colortools.py
@license  GPLv3
@brief    WRITEME
"""

from pnm_files import ppm_file
import sys

if __name__ == "__main__":
    print("Foo!\n")
    infilename = "./test/test.ppm"
    myppm = ppm_file()
    myppm.loadimage(infilename)
    print(type(myppm))
    print(type(myppm.img))
    print(type(myppm.img.data))
    print("DATA SIZE: %d %d %d" % (len(myppm.img.data),
                                   len(myppm.img.data[0]),
                                   len(myppm.img.data[0][0])))
    print("R %d, G %d, B %d\n" % (myppm.img.data[0][0][0],
                                  myppm.img.data[0][0][1],
                                  myppm.img.data[0][0][2]))
    myppm.img.adj_hue_deg(180.0)
    myppm.saveimage("./test/out.ppm")
    sys.exit(0)
