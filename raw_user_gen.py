#!/usr/bin/python2.6

##  raw_user_gen.py - Statistic Generation Script
##  Last revised: 2012-03-22
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



## Writes summary statistics to a new table
## Use in crosstab analysis of license usage
## not part of the core web-based monitoring tool

import os, sys, string, re, cgi, MySQLdb, json, datetime, time, calendar
from LicMonitor import connectLicenseStorage # LicMonitor.py module

dLogBegin = time.strptime("2011-09-22 00:00:00", "%Y-%m-%d %H:%M:%S")
dLogUntil = time.strptime("2011-11-30 21:00:00", "%Y-%m-%d %H:%M:%S")

conn = connectLicenseStorage()
cursor = conn.cursor()

dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

inc = 0
timecursor = time.mktime(dLogBegin)
# headers for CSV output
print ",".join(["ID", "YEAR", "MONTH", "DAY", "DOW", "HOUR", "MIN", "ROWANCLOUD", "ROB302", "ROBGEO", "ROB301", "ROB311" ])
while(timecursor < time.mktime(dLogUntil)):
	timecursor = timecursor+300
	
	sql = """SELECT `time`, SUM(`action`) AS `STATUS`, `user`, `computer`, `uid` FROM `license`.`license_monitor` WHERE `license` = 'ArcInfo' and `time` > '""" + time.strftime("%Y-%m-%d %H:%M:%S", dLogBegin) + """' and `time` < '""" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(timecursor) ) + """' GROUP BY `uid`;"""
	cursor.execute(sql)

	timetuple = time.gmtime(timecursor)
	usercount = []
	usercount.append(timetuple[0]) # 0 year
	usercount.append(timetuple[1]) # 1 month
	usercount.append(timetuple[2]) # 2 day
	usercount.append(dow[timetuple[6]]) # 3 day of week
	usercount.append(timetuple[3]) # 4 hour
	usercount.append(timetuple[4]) # 5 day
	# extra empty slots for summing up room-by-room counts
	usercount.append(0) # 6 rowancloud
	usercount.append(0) # 7 rob 302
	usercount.append(0) # 8 rob geo
	usercount.append(0) # 9 rob 301
	usercount.append(0) # 10 rob 311
### The above slots should correspond to your groups as defined in query_users
### This will then produce a CSV file that can be used in Excel's PivotTable

	results = cursor.fetchall()
	for r in results:
		if(r[1]):
			if(r[3][:6] == "rcloud"):
				usercount[6] = usercount[6]+1
			if(r[3][:10] == "robilab302"):
				usercount[7] = usercount[7]+1
			if(r[3][:10] == "robilabgeo"):
				usercount[8] = usercount[8]+1
			if(r[3][:10] == "robilab301"):
				usercount[9] = usercount[9]+1
			if(r[3][:10] == "robilab311"):
				usercount[10] = usercount[10]+1	
	
	print "".join([str(inc), ",", ",".join("%s" % item for item in usercount)])
	inc = inc + 1

