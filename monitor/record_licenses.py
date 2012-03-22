#!/usr/bin/python

##  record_licenses.py - script reads from lmstat, stores number of licenses in rrd db
##  Last revised: 2011-05-26
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


import os, sys, string, rrdtool

# specify your own set of licenses to monitor; alter 'term' value as needed
# remember to change the 'db' value as it is the filename.rrd

### the values in the 'db' key constitute the names of the licenses used throughout this monitoring tool
### e.g. licenses = map(lambda x: x['db'], search)
search = [ { 'term':"Users of ARC/INFO:", 'val':10, 'max':5, 'db':'GISArcInfo' },
			{'term':"Users of Grid:", 'val':10, 'max':5, 'db':'GISSpatial' },
			{'term':"Users of Maplex:", 'val':10, 'max':5, 'db':'GISMaplex' },
			{'term':"Users of Network:", 'val':10, 'max':5, 'db':'GISNetwork' },
			{'term':"Users of TIN:", 'val':10, 'max':5, 'db':'GIS3D' },
			{'term':"Users of imess:", 'val':10, 'max':5, 'db':'Imagine' },
			{'term':"Users of 81000ESCSE_F:", 'val':10, 'max':5, 'db':'AutoCAD' },] # autocad on license2
rrddir='/var/www/html/licenses/monitor/rrd/'

for line in sys.stdin.readlines():
    for x in search:
        if not os.path.exists(rrddir + x['db'] + '.rrd'):
            rrdtool.create( rrddir + x[ 'db' ] + '.rrd', '-s 300', '-b 1304208000',
            'DS:value:GAUGE:600:U:U', \
            'RRA:MAX:0.5:1:600', 'RRA:MAX:0.5:6:700', 'RRA:MAX:0.5:24:775', 'RRA:MAX:0.5:288:797' )
        if x[ 'term' ] in line:
            cols = line.split()
            rrdtool.update( rrddir + x[ 'db' ] + '.rrd', '--template=value', 'N:' + cols[ x [ 'val' ] ])

