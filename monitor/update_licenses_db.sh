#!/bin/bash

### this updates your rrd databases
/opt/license/arcgis/license10.0/bin/lmutil lmstat -a | /var/www/html/licenses/monitor/record_licenses.py

### this updates your MySQL db
/var/www/html/licenses/monitor/track_users_mysql.py
