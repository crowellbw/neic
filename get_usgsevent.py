#!/home/crowellb/anaconda3/bin/python3
import json
import urllib.request 


def eventinformation(eventid):
	m={}
	ot={}
	loc={}
	lon={}
	lat={}
	dep={}
	indexist=0
	with urllib.request.urlopen("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_week.geojson") as url:
		jsondata = json.loads(url.read().decode())
		for f in jsondata['features']:
			props =  f['id']
			if (eventid == props):
				m = f['properties']['mag']
				ot = f['properties']['time']
				loc = f['geometry']['coordinates']
				lon = loc[0]
				lat = loc[1]
				dep = loc[2]
				indexist = 1
	return(m,ot,lon,lat,dep,indexist)


#a = eventinformation('us70005myn')

#print (a)
