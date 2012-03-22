#!/usr/bin/python

##  render_graphs.py - updates rrd graphs, serves them up
##  last revised: 2012-03-22
##  Copyright (C) 2012 John Reiser, <reiser@rowan.edu>
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##  
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys, cgi, time, rrdtool
import cgitb
cgitb.enable()
q = cgi.FieldStorage()

### filesystem locations and website location
url = "/licenses/" # with trailing slash
imgdir = "/var/www/html/licenses/"
rrddir = "/var/www/html/licenses/monitor/rrd/"

### list of license types monitored
licenses = ['GISArcInfo', 'GISSpatial', 'GIS3D', 'GISNetwork', 'GISMaplex', 'AutoCAD', 'Imagine']

tframes = {'24hours':300, '7days':2100, '1month':9000, '1year':109500} #key: text of timeframe, value: refresh rate
period = '24hours'

if q.getfirst('period') in tframes.keys():
	period = q.getfirst('period')
if "license" in q:
	if q["license"].value in licenses:
		l = q["license"].value
		fn = imgdir+l+"-"+period+".png"
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
						  'DEF:value='+rrddir+l+'.rrd:value:MAX',
						  'AREA:value#3F1A0A') ### customize the colors here; refer to rrdtool documentation
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
