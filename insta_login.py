
'''

Save info into ftp

'''


import ftplib
import io
import requests

import os
import sys
import time
import datetime
import json

from random import shuffle

# ------------------------------------------------------------------------------------

import socket
print((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

# ------------------------------------------------------------------------------------

sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

bot = Bot()

#TXT File Path ///
filePath = os.path.dirname(os.path.abspath(__file__)) + "/"

bot.login(username="1nsta_bot001", password="Insta12#")