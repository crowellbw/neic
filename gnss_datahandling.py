#!/home/crowellb/anaconda3/bin/python3
import json
def findstations(sitemetadata,gpstime):
        return(SITES,LATS,LONS,DIST)


def getdata(gpstime,sites):
        return()

def readmetadata(sitemetadata):
	stalons = list()
	stalats = list()
	staalts = list()
	staids = list()
	with open (sitemetadata) as json_file:
		jsondata = json.load(json_file)
		for f in jsondata['features']:
			props =  f['properties']
			staids.append(str(props['siteid']))
			stalons.append(float(props['lon']))
			stalats.append(float(props['lat']))
			staalts.append(float(props['alt']))
	return(staids,stalons,stalats,staalts)
