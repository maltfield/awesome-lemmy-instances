#!/usr/bin/env python3
################################################################################
# File:    generate_readme.py
# Version: 0.1
# Purpose: Creates the README.md file for this repo
# Authors: Michael Altfield <michael@michaelaltfield.net>
# Created: 2023-06-06
# Updated: 2023-06-06
################################################################################

################################################################################
#                                   IMPORTS                                    #
################################################################################

import json

################################################################################
#                                  SETTINGS                                    #
################################################################################

LEMMY_STATS_CRAWLER_FILENAME = 'lemmy-stats-crawler.json'

################################################################################
#                                  FUNCTIONS                                   #
################################################################################

################################################################################
#                                  MAIN BODY                                   #
################################################################################

##################
# CHECK SETTINGS #
##################

####################
# HANDLE ARGUMENTS #
####################

#####################
# DECLARE VARIABLES #
#####################

readme_contents = ''

readme_contents += "| Instance | Adult | \n"
readme_contents += "| :---: | :---: | \n"

################
# PROCESS JSON #
################

with open( LEMMY_STATS_CRAWLER_FILENAME ) as json_data:
	data = json.load(json_data)

for instance in data['instance_details']:

	domain = instance['domain']
	name = instance['site_info']['site_view']['site']['name']
	federation_enabled = instance['site_info']['site_view']['local_site']['federation_enabled']

	if federation_enabled == True:
		federated_linked = instance['site_info']['federated_instances']['linked']
		federated_allowed = instance['site_info']['federated_instances']['allowed']
		federated_blocked = instance['site_info']['federated_instances']['blocked']
	else:
		federated_linked = []
		federated_allowed = []
		federated_blocked = []

	registration_mode = instance['site_info']['site_view']['local_site']['registration_mode']
	slur_filter = instance['site_info']['site_view']['local_site']['slur_filter_regex']
	community_creation_admin_only = instance['site_info']['site_view']['local_site']['community_creation_admin_only']
	enable_downvotes = instance['site_info']['site_view']['local_site']['enable_downvotes']
	enable_nsfw = instance['site_info']['site_view']['local_site']['enable_nsfw']

	#print( instance['site_info']['site_view']['local_site'] )

	# is this instance adult-friendly?
	if slur_filter != None or enable_nsfw != True:
		adult = 'No'
	else:
		adult = 'Yes'

	readme_contents += "| [" +name+ "](" +domain+ ") "
	readme_contents += "| " +adult
	readme_contents +=  " |\n"

with open( "README.md", "w" ) as readme_file:
	readme_file.write( readme_contents )
