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

readme_contents = '''
# Awesome Lemmy Instances

This repo was created to help users migrate from reddit to lemmy (a federated reddit alternative).

Because lemmy is federated (like email), there are many different websites where you can register your new lemmy account. In general, it doesn't matter too much which server you register with. Just like with email, you can interact with users on other servers (eg hotmail, aol, gmail, etc).

However, each server has their own policies. The table below will help you compare each site to decide where to register your new lemmy account.

### Terms

 * Instance = A lemmy instance is a website that runs the lemmy software
 * Community = Each instance has many communities. in reddit, communities were called subreddits.
 * NSFW = Not Safe For Work

### Legend

 * **Adult** "Yes" means there no profanity filters or blocking of NSFW content. "No" means that there are profanity filters or NSFW content is not allowed.
 * **New Comm** "Yes" means that you can create a new community. "No" means that only admins can create new communities on this instance.

'''

readme_contents += "| Instance | Adult | New Comm | \n"
readme_contents += "| :---: | :---: | \n"

################
# PROCESS JSON #
################

import os
print( os.path.dirname(os.path.realpath(__file__)) )
print( os.getcwd() )
print( os.listdir() )


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
