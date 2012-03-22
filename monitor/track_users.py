#!/usr/bin/python2.4

##  track_users.py - script reads from lmstat, stores users/computers in serialized file
##  last revised: 2011-05-28 01:22:49 
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

## this is no longer used by default
## I'm keeping it in here in case someone does not want to use a DB for tracking this data. -reiser

import os, sys, string, cPickle, subprocess

search = [{ 'term':") (gis.rowan.edu", 'name':0, 'computer':1, 'alt':2 }	]
curid = [] # array for current IDs
users = {} # dict for user data
store = "/disk2/monitor/recent_users"

if os.path.exists(store):
	f = open(store, "r")
	users = cPickle.load(f)
	f.close()

for line in os.popen("/disk2/license/arcgis/license10.0/bin/lmutil lmstat -f ARC/INFO").readlines():
	for x in search:
		if x[ 'term' ] in line:
			cols = line.split()
			id = cols[x['name']] + '@' + cols[x['computer']]
			if id not in curid:
				curid.append(id)
			if id in users:
				users[ id ]['count'] += 1
			else: 
				users[ id ] = {}
				if cols[x['name']] == "ACTIVATED": # added to handle borrowed licenses. 
					users[ id ]['name'] = "Borrowed"
					users[ id ]['computer'] = cols[x['alt']]
				else:
					users[ id ]['name'] = cols[x['name']]
					users[ id ]['computer'] = cols[x['computer']]
				users[ id ]['count'] = 1
for u in users.keys():
	if u not in curid:
		del users[u]

f = open(store, "w")
cPickle.dump(users, f)
f.close()
