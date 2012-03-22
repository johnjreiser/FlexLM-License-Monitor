#!/usr/bin/python2.6

##  query_users.py - Script reads from mysql table, tabulates time on computer, etc
##  Revision: 02
##  Last Revised: 2012-03-22
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

import os, sys, string, re, cgi, MySQLdb, json, datetime, time, calendar
from LicMonitor import neatTime, connectLicenseStorage # LicMonitor.py module

import cgitb
cgitb.enable()

q = {}
form = cgi.FieldStorage()

defaultSoftware = "ArcInfo" # default license to query

# if there is some order to users' computer names, you can group them by prefix
computer_groups = ['robilab301', 'robilab302', 'robilabgeo', 'robilab311', 'rcloud']

dLogDays = -30 # default number of days to return in the log, always negative
dLogUntil = datetime.datetime.now()
dLogBegin = (dLogUntil+datetime.timedelta(dLogDays))

print "Content-Type: text/plain\n"
#print "Content-Type: application/json\n"

if "license" in form:
	temp = re.search('[\w\-]+', form["license"].value)
	if temp.group(0):
		q["license"] = temp.group(0)[:20]
	else:
		q["license"] = defaultSoftware
else:
	q["license"] = defaultSoftware

if "online" in form:
	if form["online"].value == 'now':
		q["online"] = 'now'

if "user" in form:
	temp = re.search('[\w\-]+', form["user"].value)
	if temp.group(0):
		q['user'] = temp.group(0)[:20].lower()

if "computer" in form:
	temp = re.search('[\w\-]+', form["computer"].value)
	if temp.group(0):
		q['computer'] = temp.group(0)[:20].lower()

if "group" in form:
	temp = re.search('[\w\-]+', form["group"].value)
	if temp.group(0) in computer_groups:
		q['group'] = temp.group(0)[:20].lower()

if "day" in form:
	delta = -1
	if "range" in form:
		delta = re.search('\d+', form["range"].value)
		delta = int(delta.group(0))*-1
	enddate = re.search('\d{4}\-\d{2}\-\d{2}', form["day"].value)
	enddate = enddate.group(0)
	enddate = enddate.split("-")
	for i in range(0,len(enddate)):
		enddate[i] = int(enddate[i])
	dLogUntil = datetime.date(enddate[0], enddate[1], enddate[2])
	dLogBegin = (dLogUntil+datetime.timedelta(delta))

if "computer" in q and "user" in q:
	sql = """SELECT `time`, `action`, `computer` FROM `license`.`license_monitor` WHERE `computer` = '""" + \
		q["computer"] + """' and `user` = '""" + q["user"] + """' and `license` = '""" + q["license"] + "';"
elif "user" in q:
	sql = """SELECT `time`, `action`, `computer` FROM `license`.`license_monitor` WHERE `user` = '""" + \
		q["user"] + """' and `license` = '""" + q["license"] + "' and `time` > '"+ dLogBegin.isoformat()+"' and `time` < '"+dLogUntil.isoformat()+"';"
elif "group" in q:
	sql = """SELECT `time`, `action`, `computer`, `user`, `uid` FROM `license`.`license_monitor` WHERE `computer` LIKE '""" + \
		q["group"] + "%' and `license` = '""" + q["license"] + "';"
elif "online" in q:
	if q["online"] == 'now':
		sql = """SELECT `time`, `user`, `computer`, `uid` FROM `license`.`UsersOnline` WHERE `license` = '""" + q["license"] + "' AND STATUS = 1;"
	if q["online"] == "date":
		sql = """SELECT `time`, SUM(`action`) AS `action`, `user`, `computer`, `uid` FROM `license`.`license_monitor` WHERE `license` = '""" + q["license"] + "' and `time` > '"+ dLogBegin.isoformat()+"' and `time` < '"+dLogUntil.isoformat()+"' and `action` = 1 GROUP BY `uid`;"
else:
	sys.exit()

conn = connectLicenseStorage()
cursor = conn.cursor()

cursor.execute(sql)
## returns user, computer, license, uid, STATUS, MAX(date)
results = cursor.fetchall()

if "group" in q:
	users = {} # hash of all users, by uid
	uu = {} # hash of users, with cumulative time
	uc = [] # unique list of users
	timed = 0 # cumulative time for all users
	maxuser = {'user': '', 'seconds': 0} # max user
	for r in results: # massages output from sql
		if r[4] not in users:
			users[r[4]] = []
		users[r[4]].append(time.mktime(r[0].timetuple()))	
		if r[3] not in uu:
			uu[r[3]] = 0
		if r[2] not in uc:
			uc.append(r[2])
	for u in users.keys(): # calculates cumulative times
		un = re.search('\w+:([\w\-]+)@', u).group(1)
		if len(users[u])%2:
			users[u].append(time.mktime(datetime.datetime.now().timetuple()))
		for t in range(0,len(users[u]),2):
			timed = timed + (users[u][t+1] - users[u][t]) # cumulative time for all users
			uu[un] = uu[un] + (users[u][t+1] - users[u][t]) # cumulative time for one user
	for un in uu.keys():
		if(uu[un] > maxuser['seconds']):
			maxuser['user'] = un
			maxuser['seconds'] = uu[un]
		if "friendly" in form:
			uu[un] = neatTime(uu[un], True)
	maxuser['time'] = neatTime(maxuser['seconds'])
	output = {'group': q["group"], 'time': neatTime(timed), 'users': uu, 'computers': uc, "maxuser": maxuser}
elif "online" in q:
	log = []
	for r in results:
		t = []
		for i in r:
			t.append(i)
		t[0] = t[0].isoformat(" ")
		t[3] = neatTime(time.mktime(datetime.datetime.now().timetuple()) - time.mktime(time.strptime(t[0], "%Y-%m-%d %H:%M:%S")))
		log.append(t)
	output = {'log': log}
else:
	users = {}
	for r in results:
		if r[2] not in users:
			users[r[2]] = []
		t = []
#		for i in r:
#			t.append(i)
		t.append(r[0].isoformat(" "))
		t.append(r[1])
		users[r[2]].append(t)
	timed = 0
	for c in users.keys():
		log = users[c]
		for t in range(0,len(log),2):
			if t+1 >= len(log):
				timed = timed + (time.mktime(datetime.datetime.now().timetuple()) - time.mktime(time.strptime(log[t][0], "%Y-%m-%d %H:%M:%S")))
			else:
				timed = timed + (time.mktime(time.strptime(log[t+1][0], "%Y-%m-%d %H:%M:%S")) - time.mktime(time.strptime(log[t][0], "%Y-%m-%d %H:%M:%S")))
	output = { "time": neatTime(timed), "log": users, 'seconds': timed}
if "friendly" in form:
	print json.dumps(output, indent=2)
else:
	print json.dumps(output)
