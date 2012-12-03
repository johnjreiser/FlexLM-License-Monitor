#!/usr/bin/python

## render_graphs.py, r03 - license monitor cgi/template
## last revised: 2012-12-03
## author: John Reiser <reiser@rowan.edu>
## updates rrdgraphs
## r03: creates graph file if it does not exist

import os, sys, cgi, time, rrdtool
#import cgitb
#cgitb.enable()
q = cgi.FieldStorage()

url = "/licenses/" # with trailing slash
imgdir = "/var/www/html/licenses/"
rrddir = "/var/www/html/licenses/monitor/rrd/"

licenses = ['GISArcInfo', 'GISSpatial', 'GIS3D', 'GISNetwork', 'GISMaplex', 'CityEng']
tframes = {'24hours':300, '7days':2100, '1month':9000, '1year':109500} #key: text of timeframe, value: refresh rate
period = '24hours'

if q.getfirst('period') in tframes.keys():
	period = q.getfirst('period')
if "license" in q:
	if q["license"].value in licenses:
		l = q["license"].value
		fn = imgdir+l+"-"+period+".png"
		if(not os.path.exists(fn)):
			tempfile = open(fn, "w")
			tempfile.write("")
			tempfile.close()
		if ((time.time()-os.stat(fn).st_mtime)>tframes[period]):
			try:
				rrdtool.graph(fn, 
						  '--imgformat', 'PNG',
						  '--width', '600',
						  '--height', '200',
						  '-s', "-"+period,
						  '-l', '0', # no negative values, ever
						  '-u', '3', # max 3 y-axis by default 
						  '-Y', 
						  '--title', l+' Licenses in Use',
						  '--font', 'DEFAULT:0:Utopia',
						  'DEF:value='+rrddir+l+'.rrd:value:MAX',
						  'AREA:value#3F1A0A')
			except:
				pass
		image = open(fn, 'rb').read()
		print "Content-Type: image/png\nContent-Length: %d\n" % len(image)
		print image
	else:
		print "Content-Type: text/plain\n"
		print "Invalid graph requested."
else:
	print "Content-Type: text/plain\n"
	print "Invalid request."
