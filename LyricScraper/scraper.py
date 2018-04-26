from bs4 import BeautifulSoup
import requests
from time import time
from time import sleep
import random
import pandas as pd
import json

BASE_URL = "https://www.azlyrics.com/"
clauses = ["Christmas", "mixtape", "soundtrack", "compilation", "boxset"]

user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']

#USE https://free-proxy-list.net/ TO FIND TEMPORARY PROXIES. MAKE SURE THEY READ HTTPS. ELITE PROXIES PREFERRED.
proxies = [
		{"http": "http://117.6.161.118:53281"},
		{"http": "http://92.53.73.138:8118"}, 
		{"http": "http://103.86.185.190:8080"}, 
		{"http": "http://13.115.228.99:3128"},
		{"http": "http://41.193.223.86:8080"},
		{"http": "http://51.15.86.88:3128"},
		{"http": "http://85.115.15.2:8080"}]

#manual input of artist data
artist_list_manual = ["daftpunk"]
ref_to_artist = {"daftpunk":"Daft Punk", "mia":"M.I.A.", "ettajames":"Etta James", "radiohead":"Radiohead", "madonna":"Madonna", "feist":"Feist", "arianagrande":"Ariana Grande", "sufjanstevens":"Sufjan Stevesn", "vincestaples":"Vince Staples", "samsmith":"Sam Smith", "azealiabanks":"Azealia Banks", "aliciakeys":"Alicia Keys", "leonalewis":"Leona Lewis", "killers":"The Killers", "cardi-b":"Cardi B", "drake":"Drake", "leonbridges":"Leon Bridges", "rihanna":"Rihanna", "dualipa":"Dua Lipa", "arcticmonkeys":"Arctic Monkeys", "bjork":"Bjork", "gorillaz":"Gorillaz", "deathgrips":"Death Grips", "fleetfoxes":"The Fleet Foxes", "bigthief":"Big Thief", "stvincent":"St. Vincent", "carlyraejepsen":"Carly Rae Jepsen", "charlixcx":"Charli XCX", "lanadelrey":"Lana Del Rey", "angelolsen":"Angel Olsen", "sza": "Sza", "selenagomez":"Selena Gomez", "beatles": "The Beatles", "springsteen": "Bruce Springsteen", "redhotchilipeppers":"The Red Hot Chili Peppers", "queen": "Queen", "guns":"Guns N Roses", "ledzeppelin": "Led Zeppelin", "edsheeran":"Ed Sheeran", "knowles":"Beyonce", "frankocean":"Frank Ocean", "rollingstones":"The Rolling Stones", "brunomars":"Bruno Mars", "taylorswift":"Taylor Swift", "calvinharris":"Calvin Harris", "ladygaga":"Lady Gaga", "lorde":"Lorde"}

def get_artist_links(section_url):
	html = urlopen(section_url).read()
	soup = BeautifulSoup(html, "lxml")
	artist_col = soup.find("div", "artist-col")

def get_songs(proxies, user_agents, artist):
	artist_url = BASE_URL + artist[0] + "/" + artist + ".html"
	print("Searching for " + artist + "...")
	sleep(random.randint(9, 11))
	html = requests.get(artist_url, headers = {'User-Agent': random.choice(user_agents)}, proxies = random.choice(proxies)).content
	soup = BeautifulSoup(html, "lxml")
	all_div = soup.find("div",{"id":"listAlbum"})
	mixtape = False
	song_urls = []
	for item in all_div.findChildren():
		if item.name=='div':
			if item.text=="other songs:":
				return song_urls
			elif any(clause in item.text for clause in clauses):
				mixtape = True
				continue
			else:
				mixtape = False
		if item.name=="a":
			try:
				if("radiohead" not in str(item['href'][2:]) and "madonna" not in str(item['href'][2:]) and "ettajames" not in str(item['href'][2:]) and "mia" not in str(item['href'][2:])):
					continue
				elif(mixtape):
					continue
				else:
					song_urls.append("https://www.azlyrics.com" + item['href'][2:])
			except:
				pass
	return song_urls

def get_lyrics(proxies, user_agents, artist, songs):
	songinfo = []
	start_time = time()
	count = 0
	for songurl in songs:
		count += 1
		sleep(random.randint(9, 14))
		elapsed_time = time() - start_time
		print('Request: {}; Frequency: {} requests/s'.format(count, count/elapsed_time))
		html = requests.get(songurl, headers = {'User-Agent': random.choice(user_agents)}, proxies = random.choice(proxies)).content
		soup = BeautifulSoup(html, "lxml")
		title = soup.find('div', {'class': "ringtone"}).findNext("b").text
		title = title.replace('"', "")
		lyrics = str(soup.find('div', {'class': "ringtone"}).findNext("div").text)
		songinfo.append({"title":title, "artist":ref_to_artist[artist], "lyrics":lyrics})
	return songinfo

def scrape(proxies, user_agents, artists):
	scraped_data = []
	for artist in artist_list_manual:
		songurls = get_songs(proxies, user_agents, artist)
		songdict = get_lyrics(proxies, user_agents, artist, songurls)
		scraped_data = scraped_data + songdict
		data_to_json(scraped_data)
	return scraped_data

#CURRENTLY ONLY WRITES NEW DATA IDK HOW TO APPEND 
def data_to_json(data):
	with open("scrapeddata.json", "w") as outfile:
		json.dump(data, outfile)

def main():
	print("Starting scraping process...")
	song_data = scrape(proxies, user_agents, artist_list_manual)
	data_to_json(song_data)
	print("DONE.")

if __name__ == "__main__":
	main()

