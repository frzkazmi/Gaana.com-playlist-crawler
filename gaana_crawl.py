#!/usr/bin/python
#dev Ashish_G
import sys
import subprocess
try:
	import urllib2
	from bs4 import BeautifulSoup
except ImportError as E:
	print("Library not installed. Please check prequisites before running this script: "+E)
	sys.exit(1)
cache_flag=True
log_flag=True
baseurl="http://gaana.com"
youtube_search="https://www.youtube.com/results?search_query="
youtube_base="https://www.youtube.com"
def genCache(write):
	chart_links=[]
	chart_title=[]
	if write:
		b_file=open("cache.dat","w")
	tmp_=urllib2.urlopen(baseurl+"/topcharts")
	charts=tmp_.read()
	soup=BeautifulSoup(charts,'lxml')
	div="featured_playlist_data"
	for pun in soup.findAll("div",{"class":div}):
		l=pun.find("a",{"class":"pjax"})['href'].encode('utf')
		chart_links.append(l)
		chart_title.append(pun.find("span",{"class":"pjax"})['title'])
		try:
			if write:
				b_file.write(chart_title[-1]+":"+chart_links[-1]+"\n")
		except:
			continue
	if write:
		b_file.close()
	return chart_title,chart_links  	
def grabYoutubeURL(query):
	url="https://www.youtube.com/results?search_query="+query
	cls="yt-uix-tile-link"
	o=urllib2.urlopen(url)
	resp=o.read()
	soup=BeautifulSoup(resp,'lxml')
	div = soup.find("a",{"class":cls})
	return str(youtube_base+div['href'])
def downloadNow(youtube_link,dir):
	output_path=dir
	subprocess.call(['youtube-dl',"-x","-o", dir+"/%(title)s.%(ext)s'","--extract-audio","--audio-format","mp3",youtube_link])  
def fetchFromCache(file):
	chart_links=[]
	chart_title=[]
	c1=b_file.read().split("\n")
	for line in c1:
		chart_title.append(line.split(":")[0])
		chart_links.append(line.split(":")[-1])
	file.close()
	return chart_title,chart_links
chart_links=[]
chart_title=[]
if cache_flag:
	try:		
		b_file=open("cache.dat","r")	
		print("Cache found! Fetching from cache...\n")
		chart_title,chart_links=fetchFromCache(b_file)
	except IOError:
		print("Cache not found! Caching...")
		chart_title,chart_links=genCache(True)
else:
	chart_title,chart_links=genCache(True)
print("\n********************  Top Charts  **************************\n")
i=1
for name in chart_title:
	if name=="":
		continue
	print(str(i)+". "+name)
	i+=1
while True:
	c=int(raw_input("Select list (1-"+str(i-1)+"): "))
	if c>=len(chart_links):
		print("Enter valid Input!")
		continue
	if c<0:
		print("Enter valid Input!")
		continue
	break
url=chart_links[c-1]
chart_name=chart_title[c-1]
print("\nFetching Songs List. Please wait...")
response = urllib2.urlopen(baseurl+url)
content = response.read()
print("\n*******************  Songs List  **************************\n")
soup=BeautifulSoup(content,'lxml')
container_class="inn-content content-container"
songList=soup.find('div',{"class":container_class})
y_qry=[]
songs=[]
count=1
for hgrp in songList.findAll("hgroup"):
	try:
		songCurr=hgrp.h2.a['title']
		
	except KeyError, e:
		pass	
	i=0
	for artGrp in hgrp.findAll("a",{"class":"pjax a-d1 _artist"}):
		if i==0:
			artist=artGrp['title']
		else: 
			artist+=","+artGrp['title']
		i+=1
	songCurr=artist+"-"+songCurr
	songs.append(songCurr)
	print(str(count)+". "+songCurr)	
	count+=1		
	y_qry.append("+".join(songCurr.split(" "))+"+audio+only")
#print("\nTotal: "+str(len(songs))+" songs will be downloaded\n ")
dirname=str(raw_input("Enter directory name:"))
if dirname=="":
	dirname="Downloads"
if " " in dirname:
	dirname=dirname.split(" ")[0]
print("\nStarting with download...")
ps=0
if log_flag:
	log=open("log.txt","w")
	
for sng in songs:
	try:
            ch=int(raw_input("Enter 1. for downloading whole playlist  2. for a particular song "))
            if ch==1:
                	
		print("\n**************************************************************")
		print("**************** Downloading "+str(ps+1)+" of "+str(len(songs))+" ******************")
		print("**************************************************************")
		print("\nScraping download url for "+sng)
		yurl=grabYoutubeURL(y_qry[ps])
		print("Subprocess call...")
		downloadNow(str(yurl),str(dirname))
		if log_flag:
			log.write("Downloaded: "+dirname+"//"+sng)
	    elif ch==2:
                index = int(raw_input("Enter index of song "))
                yurl=grabYoutubeURL(y_qry[index-1])
		print("Subprocess call...")
		downloadNow(str(yurl),str(dirname))
		
	    else:
                
                print "Wrong choice"
                log.write("Wrong choice")
	except Exception as e:
		#print(e)
		
		print("Error while downloading: "+sng+"! Will resume for the next one though!")
		
		ps+=1
		
	ps+=1
if log_flag:
	log.close()
print("\n\n************************** Success All! ******************************")
# EOF
