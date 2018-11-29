from bs4 import BeautifulSoup
import requests
import csv
import re
import time
import random

link_array = []

req_headers = {
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.8',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		}

def roll_thru(num):
	source = requests.get('https://www.mtsamples.com/site/pages/browse.asp?type=95%2DRadiology&page={0}'.format(num),headers=req_headers).text
	soup = BeautifulSoup(source, 'lxml')
	table = soup.find('table',id='Browse')
	links = table.find_all('a')	
	for link in links:
		updated = 'https://www.mtsamples.com' + link['href']
		link_array.append(updated)

def get_main_links():
	verify = 1
	while verify < 29:
		roll_thru(verify)
		verify+=1
		time.sleep(random.randint(10,50))

	with open('get_links.csv', 'w') as write:
			csv_writer = csv.writer(write)
			for item in link_array:
				csv_writer.writerow(item)
			
#get_main_links()

def get_data(link):
	req_headers = {
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.8',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
		}
	source = requests.get('{0}'.format(link),headers=req_headers).text
	soup = BeautifulSoup(source, 'lxml')
	table = soup.find('div',id='sampletext')
	current_text = table.text
	get_name = re.search(r'Sample Name: .* D', current_text)
	if get_name:
		name_group = get_name.group()
	else:
		grab_link = re.search(r'Sample=.*',link)
		elim = grab_link.group()
		next_step = re.search(r'-.*', elim)
		change = next_step.group()
		name_group = change[1:]
	minus_d = name_group[0:len(name_group)-1]
	get_des = re.search(r'Description:.*\.', current_text)
	if get_des:
		des_form = get_des.group()
	else:
		diff = re.search(r'Description:.*\n', current_text)
		des_form = diff.group()
	get_rest = re.search(r't\)\n*.*', current_text)
	if get_rest:
		formatted = get_rest.group()
		formatted = formatted[2:]
		formatted = formatted.replace('\n','')
		formatted = formatted.replace('\r','')
		entry = [minus_d, des_form, formatted]
		return entry
	else:
		print(current_text)
		

def get_stored_links():
	save_stuff = []
	with open('get_links.csv', 'r') as f:
		for line in f:
			if line != '\n':
				wo_comma = line.replace(',','')
				save_thing = get_data(wo_comma)
				save_stuff.append(save_thing)
	with open('final.csv', 'w') as write:
			csv_writer = csv.writer(write)
			csv_writer.writerow(['Name','Description','Details'])
			for item in save_stuff:
				try:
					csv_writer.writerow([item[0],item[1],item[2]])
				except UnicodeEncodeError:
					item[0] = item[0].replace('\x92', '')
					item[1] = item[1].replace('\x92', '')
					item[2] = item[2].replace('\x92', '')
					item[0] = item[0].replace('\x93', '')
					item[1] = item[1].replace('\x93', '')
					item[2] = item[2].replace('\x93', '')
					item[0] = item[0].replace('\x94', '')
					item[1] = item[1].replace('\x94', '')
					item[2] = item[2].replace('\x94', '')
					csv_writer.writerow([item[0],item[1],item[2]])
get_stored_links()
