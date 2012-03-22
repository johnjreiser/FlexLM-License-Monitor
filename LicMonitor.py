##  LicMonitor.py - common functions for the FlexLM License Monitor tool.
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

import MySQLdb
### change the connection information for your MySQL instance/database here
### this connection can be made with a read-only user
def connectLicenseStorage():
        return MySQLdb.connect(host='localhost', user='license', passwd='licenses', db='license')
### end connection info

def neatTime(dtime, short=False):
	"""Neatly format time (in seconds) into a more human readable format."""
	days = int(dtime/86400)
	hours = int((dtime%86400)/3600)
	minutes = int(((dtime%86400)%3600)/60)
	seconds = int((dtime%86400)%60)

	if(short):
		if days:
			ftime = "%sd %02d:%02d:%02d" % (days, hours, minutes, seconds)
		else:
#			ftime = "%ss" % seconds
			ftime = ''
			if not minutes and not hours:
				ftime = "%ss" % seconds
			if minutes:
				ftime = "%sm" % minutes + ftime
			if hours:
				if minutes == 0:
					ftime = "0m"+ftime
				ftime = "%sh" % hours + ftime
	else:
		if days:
			ftime = "1 day" if days==1 else str(days) + " days"
			if hours:
				ftime = ftime+", 1 hour" if hours==1 else ftime+", "+str(hours) + " hours"
		elif not days and hours:
			ftime = "1 hour" if hours==1 else str(hours) + " hours"
			if minutes:
				ftime = ftime+", "+str(minutes) + " minute" if minutes==1 else ftime+", "+ str(minutes) + " minutes"
		elif not days and not hours and minutes:
			ftime = "1 minute" if minutes==1 else str(minutes) + " minutes"
			if seconds:
				ftime = ftime+", "+"1 second" if seconds==1 else ftime+", "+ str(seconds) + " seconds"
		elif not days and not hours and not minutes and seconds:
			ftime = "1 second" if seconds==1 else str(seconds) + " seconds"
		else:
			ftime = "0 seconds"
	return ftime # + " %s - %s:%s:%s:%s" % (dtime, days, hours, minutes, seconds)
