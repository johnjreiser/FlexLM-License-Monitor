#!/usr/bin/python2.6

##  track_users_mysql.py - script reads from lmstat, stores users/computers in mysql table
##  last revised: 2011-09-22
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

import os, sys, string, subprocess, MySQLdb

search = [ { 'term':") (", 'user':0, 'computer':1, 'alt':2 } ]
curid = [] # array for current IDs
users = {} # dict for user data

### monitors contains the list of license servers.
### key is the friendly name for the license server
### value is the path to the lmutil executable
### note that you can connect to a remote license server, see "AutoCAD" below, which is a remote license server
monitors = {"ArcInfo": "/opt/license/arcgis/license10.0/bin/lmutil lmstat -f ARC/INFO", \
		"ERDAS": "/opt/license/arcgis/license10.0/bin/lmutil lmstat -f imess"}#, \
#		"AutoCAD": "/disk2/license/arcgis/license10.0/bin/lmutil lmstat -a -c @'license2.rowan.edu' -f 81000ESCSE_F" }

### configure the license monitor db connection info here
### this is not using LicMonitor.py as this script makes changes to the DB
conn = MySQLdb.connect(host='localhost', user='license', passwd='licenses', db='license')
cursor = conn.cursor()

cursor.execute("""SELECT * FROM `license`.`UsersOnline` WHERE STATUS = 1;""")
## returns user, computer, license, uid, STATUS, MAX(date)
results = cursor.fetchall()
for r in results:
	id = r[3]
	users[id] = {'user':r[0], 'computer':r[1], 'status':int(r[4]), 'license':r[2]}

for license in monitors.keys():
	for line in os.popen(monitors[license]).readlines():
		for x in search:
			if x[ 'term' ] in line:
				cols = line.split()
				if cols[x['user']] == "ACTIVATED": # added to handle borrowed licenses. 
					cols[x['user']] = "borrowed"
					cols[x['computer']] = cols[x['alt']]
				id = license + ":" + cols[x['user']].lower() + '@' + cols[x['computer']].lower()
				if id not in curid:
					curid.append(id)
				if id in users:
					users[ id ]['status'] = 0
					users[ id ]['license'] = license
				else: 
					users[ id ] = {}
					users[ id ]['user'] = cols[x['user']].lower()
					users[ id ]['computer'] = cols[x['computer']].lower()
					users[ id ]['status'] = 1
					users[ id ]['license'] = license
for u in users.keys():
	if u not in curid:
		users[u]['status'] = -1

updates = []

for id in users:
	## license will change depending on software tracked, for now, just ArcInfo
	## uid format in database will be license:user@computer (varchar62)
	uid = users[id]['license'] + ":" + users[id]['user'] + "@" + users[id]['computer']
	if(users[ id ]['status'] != 0):
		updates.append((users[id]['user'], users[id]['computer'], users[id]['license'], uid, users[id]['status']))

#print updates
cursor.executemany("""INSERT INTO license_monitor (user, computer, license, uid, action) VALUES (%s, %s, %s, %s, %s)""",
	updates)
conn.commit()