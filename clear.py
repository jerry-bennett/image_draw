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

    epd = epd4in0e.EPD()   
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd4in0e.epdconfig.module_exit(cleanup=True)
    exit()
