
'''
get user details through userid list and save int in the ftp
Save info into ftp
'''

import ftplib
import io
import requests
import re
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

bot.login(username="1nsta_bot002", password="Insta12#")

MAX_RETRIES = 100
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES)
session.mount('https://', adapter)
session.mount('http://', adapter)

def replace_with_byte(match):
    return chr(int(match.group(0)[1:], 8))

def repair(brokenjson):
    return invalid_escape.sub(replace_with_byte, brokenjson)

def removeUni (str_content):

	ls = len (str_content)
	str_content = str_content.replace('\n', ' ')
	uniArray = []

	# Get all Unicode from string and creating and array
	for x in range(0, ls):
		f = str_content.find(r'\u')
		rep = str_content[f:f+6]
		uniArray.append(rep)
		str_content = str_content.replace(rep,'')

	uniArray = [x for x in uniArray if x] # Remove empty items from array

	return (str_content)


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


def get_url_from_bio(bio):

	match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', bio)

	if match is None:
		url = ''
	else:
		url = match.group(0)

	return url

def get_item_json_resp(resp, item):
	if item in json.dumps(resp):
		return json.dumps(resp[item])
	else:
		return "none"

def get_public_email_from_response(resp):
	if "public_email" in str(resp):
		data = str(resp['public_email'])
		data = data.replace('"','').rstrip()
	else:
		data = '-'
	return data

def get_email_from_bio(bio):
	match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', bio)
	if match is None:
		email = ''
	else:
		email = match.group(0)
	return email

def get_fb_email(url):
	email =""
	url = url.replace('"','')

	if url.find("facebook.com/") > 1:
		if url[-1] == '/':
			url = url + "about"
		else:
			url = url + "/about"
		u = session.get(url)

		ucontent = str(u.content)
		ucontent = ucontent.replace('&#064;','@')
		match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', ucontent)

		if match != None:
			email = match.group(0)

	return email

def get_user_info(user_id):

	sUrl = "http://i.instagram.com/api/v1/users/" + str(user_id) + "/info/"
	rUrl = session.get(sUrl) # Response URL

	user_id = ''

	if rUrl.status_code == 429:
		return "429"

	if rUrl.status_code == 200:

		d = rUrl.content
		r = json.loads(d.decode('utf-8'))

		data = json.dumps(r['user'])

		return data

def check_user(user_id):

	user_info = bot.get_user_info(user_id)

	# user_info = get_user_info(user_id)

	# print (json.dumps(user_info))


	if "'category':" in str(user_info):
		return json.dumps(user_info['category'])
	else:
		return "none"




#---- Config ----

now = datetime.datetime.now()
date_time = str(now.month) + str(now.day)+ str(now.year) +"_" +str(now.hour) + str(now.minute) + str(now.second)

def ftp_login():
	ftp = ftplib.FTP('files.000webhost.com')
	ftp.login('leosimoestn','leosim123')
	print("\nFTP - Logged in - " + ftp.getwelcome())
	ftp.cwd('insta_log')

	return ftp

def read_ftp_file (folder, filename):

	ftp = ftp_login()
	ftp.cwd(folder)
	# ftp.retrlines('LIST')

	print ("Read file: " + folder + "/" + filename)

	ftp.retrlines('RETR ' + filename, handle)

	ftp.close()

	# return data

a = 0
wl = ""	

def handle(userid):

	global wl

	sleepTime = 60
	pause = 3

	resp = bot.get_user_info(userid)


	if (resp == '429') or (resp=='400'):
		print ("Error" + resp +  " - Too many requests! // " + str(sleepTime) + " seconds standby...")
		time.sleep(sleepTime)
	else:

		username = get_item_json_resp(resp,'username').replace('"','')

		bio = removeUni(get_item_json_resp(resp,'biography'))
		full_name = removeUni(get_item_json_resp(resp,'full_name'))

		fb_email = ""

		public_email = get_public_email_from_response(resp)
		user_id = userid
		bio_email = get_email_from_bio(bio)
		bio_url = get_url_from_bio(bio)
		external_url = get_item_json_resp(resp,'external_url')

		if len(external_url) >=0:
			external_url = '-'

		if (external_url) and (len(fb_email) > 0):
			fb_email = get_fb_email(external_url)

		if (bio_url) and (len(fb_email) > 0):
			fb_email = get_fb_email(bio_url)

		check_category = check_user(userid)

		print (username)

		if check_category != 'none':
			category = check_category.lower().replace('"','').replace('/','-').replace('(','').replace(')','')
		else:
			category = 'general user'

		wl = wl + str(username) + ","
		wl = wl + full_name + ","
		wl = wl + str(userid) + ","
		wl = wl + category + ","
		wl = wl + public_email + ","
		wl = wl + bio_email + ","
		wl = wl + bio_url + ","
		wl = wl + fb_email + ","
		wl = wl + external_url
		wl = wl + "\n"

		write_line = wl.encode()

		time.sleep(pause)

		# print (wl)

	ftp = ftp_login()
	ftp.cwd('users')
	ftp.cwd('user_details')
	ftp.cwd('from_list')

	# check_if_folder_exists(hashtag, ftp)
	# ftp.cwd(hashtag)

	content = io.BytesIO(write_line)
	output_filename =  date_time + ".csv"

	ftp.storlines('STOR ' + output_filename, content)

	ftp.close()



def check_if_folder_exists(directory_name, ftp):

	if directory_name in str(ftp.nlst()):
		print (directory_name + " folder found." )
	else:
		ftp.mkd(directory_name)
		print (directory_name + " folder created.")


read_ftp_file ('followers','l30artwork_userid_followers.txt')
print ("FTP - Logged out.\n")
