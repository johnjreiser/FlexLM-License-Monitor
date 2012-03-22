FlexLM License Monitor README
Author: John Reiser <reiser@rowan.edu>

The FlexLM License Monitor will keep an ongoing record of commercial software usage. Software licenses managed with the FlexLM (lmgrd, lmutil) license software can be monitored using this tool.

The current version of this tool requires the following:
- Python
-- modules: MySQLdb, rrdtool 
- RRDtool
The script has been tested on Linux/Apache. 
For an example of this tool in action, visit: http://gis.rowan.edu/licenses/

Files contained in this project:
groups.html - displays usage by groups of computers
index.html - dashboard of usage, displays rrdgraphs, current software users
LICENSE.txt - GNU Public License, v3
LicMonitor.py - read-only DB connection information, helper functions
monitor/ - directory containing components to record and track usage
	.htaccess - prevent web access to this directory
	gislicenses.cron - cron file to run monitoring script every 5 minutes 
	record_licenses.py - updates the rrd files
	rrd - storage for your .rrd files
	track_users_mysql.py - stores current users in MySQL
	track_users.py - obsolete, stores files in flatfile using cPickle
	update_licenses_db.sh - shell file called by the cronjob
query_users.py - generates JSON with the tracking/log data
raw_user_gen.py - standalone function for producing data for crosstab analysis
README.txt - this file
refresh.png - "refresh current users" button on index.html
render_graphs.py - runs rrdtool on expired graphs, serves graphs to index.html
style.css - CSS for the pages
users.html - details on a specific user

The FlexLM License Monitor is released under the GPL v3.