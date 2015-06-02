"""
@author   Justin Zane Chudgar <justin@justinzane.com>
@file     py-colortools.py
@license  GPLv3
@brief    WRITEME
"""

from pnm_files import ppm_file
#import colorspaces

if __name__ == "__main__":
    for deg in [0.0, 120.0, 180.0, 240.0, 360.0]:
        infilename = "./test/test.ppm"
        myppm = ppm_file()
        myppm.loadimage(infilename)
        myppm.img.do_nothing()
        myppm.img.adj_hue_deg(deg)
        myppm.saveimage("./test/out_%03d.ppm" % (deg))
        print("Finished %03d degrees.\n" %(deg))
