#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = '/home/admin/Image_Draw/pic'
libdir = '/home/admin/Image_Draw/lib'
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd4in0e
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd7in3f Demo")

    epd = epd4in0e.EPD()   
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    # read bmp file 
    logging.info("reading bmp file")
    Himage = Image.open(os.path.join(picdir, '01.bmp'))
    logging.info("file found")
    epd.display(epd.getbuffer(Himage))
    time.sleep(3)
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in0e.epdconfig.module_exit(cleanup=True)
    exit()
