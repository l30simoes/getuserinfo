
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
import socks
import socket
import stem.process

SOCKS_PORT=7000# You can change the port number

tor_process = stem.process.launch_tor_with_config(
    config = {
        'SocksPort': str(SOCKS_PORT),
    },
)

socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
                      addr="127.0.0.1", #theres a ',' change it to '.' -- linkedin was being glitchy
                      port=SOCKS_PORT)
socket.socket = socks.socksocket

#Write your scraping code here -- I use BeautifulSoup for scraping

tor_process.kill()

# ------------------------------------------------------------------------------------


sys.path.append(os.path.join(sys.path[0], '../'))
from instabot import Bot

bot = Bot()

#TXT File Path ///
filePath = os.path.dirname(os.path.abspath(__file__)) + "/"

bot.login(username="1nsta_bot002", password="Insta12#")



MAX_RETRIES = 100
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)



def check_if_folder_exists(directory_name):

	if directory_name in str(ftp.nlst()):
		print (directory_name + " folder found." )
	else:
		ftp.mkd(directory_name)
		print (directory_name + " folder created.") 

# def read_ftp_file(s):
# 	print (str(s))

def get_userid_from_username(username):
	# sUrl = "http://www.instagram.com/%s/?__a=1" % (str(username.rstrip()))
	sUrl = "https://apinsta.herokuapp.com/u/%s"  % (str(username.rstrip()))
	rUrl = session.get(sUrl) # Response URL
	username = username.rstrip()
	
	user_id = ''

	if rUrl.status_code == 429:

		ctime =  datetime.datetime.now()
		currentTime = str(ctime.hour) + ":" + str(ctime.minute) + ":" + str(ctime.second) + " - " + str(ctime.day) +"/"+ str(ctime.month) +"/"+ str(ctime.year)
		print ("\n" + str(count) + ") " + username)
		print ("Error 429 - Too many requests! // " + str(sleepTime) + " seconds standby...")
		print ("START: " + startTime + " // NOW  : " + currentTime) 
		print ("\n\n")

		time.sleep(sleepTime)

	if rUrl.status_code == 200:

		d = rUrl.content
		r = json.loads(d.decode('utf-8'))

		user_id = json.dumps(r['graphql']['user']['id'])

	return user_id.replace('"','')







#---- Config ----

insta_account = 'l30.artwork'




now = datetime.datetime.now()
date_time = str(now.month) + str(now.day)+ str(now.year) +"_" +str(now.hour) + str(now.minute) + str(now.second)

output_filename = insta_account + "_userid_followers_" + date_time + ".txt"

user_id = get_userid_from_username(insta_account)

users = bot.get_user_followers(user_id)

wfile = ''

for i in range(len(users)):
	wfile = wfile + users[i] + "\n"
	

#------ Login -----
ftp = ftplib.FTP('files.000webhost.com')
ftp.login('leosimoestn','leosim123') 
print("\nLogged in - " + ftp.getwelcome() + "\n")
# ftp.cwd('tmp')

check_if_folder_exists('insta_log')
ftp.cwd('insta_log')	
#-----------

check_if_folder_exists('users')
ftp.cwd('users')

check_if_folder_exists('followers')
ftp.cwd('followers')


wfile = wfile.encode()

content = io.BytesIO(wfile)
ftp.storlines('STOR ' + output_filename, content)

print ("File saved - " + output_filename)

ftp.close()