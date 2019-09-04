#!/usr/bin/python

import os
import time
import requests
from html.parser import HTMLParser
s = requests.Session()

headers = {'user-agent': ''}
url = "https://www.feral-heart.com/presets"
pub_p_path = r'PublicPresets'
wait_time = 5

preset_urls = {}

class MyHTMLParser(HTMLParser):
	#def handle_starttag(self, tag, attrs):
		#print("Encountered a start tag:", tag)

	#def handle_endtag(self, tag):
		#print("Encountered an end tag :", tag)

	def handle_data(self, data):
		preset_urls.update({data : "https://www.feral-heart.com/presets/"+data})
		#print("Encountered some data  :", data)

def create_folder():
	if not os.path.exists(pub_p_path):
		os.makedirs(pub_p_path)

def request_index():
	r = s.get(url, headers=headers, timeout=wait_time, allow_redirects=True, verify=True, stream=True)
	return(r)

def parse_index(raw_data):
	parser = MyHTMLParser()
	parser.feed(raw_data.text)
	del preset_urls['\n']
	#print(preset_urls)

def get_version_online():
	return((s.get("https://www.feral-heart.com/presets/version.php",
						headers=headers, timeout=wait_time, allow_redirects=True, verify=True, stream=True).text))

def get_version_offline():
	pub_p_path = r'PublicPresets'
	if not os.path.exists(pub_p_path):
		return(0)
	vers_file = open("PublicPresets/version.php", 'r')
	vers_file.close()
	return(vers_file.read())

def check_version(version_on, version_off):
	if int(version_on) > int(version_off):
		return(True)
	else:
		return(False)

def download():
	for key, value in preset_urls.items():
		r = s.get(value, headers=headers, timeout=wait_time, allow_redirects=True, verify=True, stream=True)
		output = open('PublicPresets/'+key, 'w')
		output.write(r.text)
		output.close()
		time.sleep(0.001)

def main():
	off_v = get_version_offline()
	on_v = get_version_online()
	create_folder()
	if check_version(on_v, off_v) == True:
		raw = request_index()
		parse_index(raw)
		download()
	if os.name == 'posix':
		os.system("/usr/bin/wine FeralHeart.exe")
	else:
		os.system("FeralHeart.exe")

main()
