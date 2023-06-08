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
import pandas as pd

################################################################################
#                                  SETTINGS                                    #
################################################################################

LEMMY_STATS_CRAWLER_FILENAME = 'lemmy-stats-crawler.json'
LEMMY_STATS_CRAWLER_FILEPATH = 'lemmy-stats-crawler/' + LEMMY_STATS_CRAWLER_FILENAME

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

However, each server has their own local policies and configurations (for example, some lemmy instances disable the "downvote" button). The table below will help you compare each site to decide where to register your new lemmy account.

### Terms

 * Instance = A lemmy instance is a website that runs the lemmy software
 * Community = Each instance has many communities. In reddit, **communities were called subreddits**.
 * NSFW = Not Safe For Work

### Legend

 * **NU** "Yes" means that **New Users** can register accounts. "No" means that this instance is not accepting new account registrations at this time.
 * **NC** "Yes" means that you can create a **New Community**. "No" means that only admins can create new communities on this instance.
 * **Fed** "Yes" means that you can interact with other **federated** lemmy instances. "No" means that the instance is partially or fully siloed (you can only subscribe to communities on this one instance or other instances that are explicitly added to an allowlist)
 * **Adult** "Yes" means there's no **profanity filters** or blocking of **NSFW** content. "No" means that there are profanity filters or NSFW content is not allowed. Note: "Yes" does not mean all NSFW content is allowed. Each instance may block some types of NSFW content, such as pornography. Additionally, you can configure your account to hide NSFW content. 
 * **↓V** "Yes" means this instance **allows downvotes**. "No" means this instance has turned-off downvote functionality.
 * **Users** The **number of users** that have been active on this instance **this month**. If there's too few users, the admin may shutdown the instance. If there's too many users, the instance may go offline due to load. Pick something in-between.

Download table as <a href="https://raw.githubusercontent.com/maltfield/awesome-lemmy-instances/main/awesome-lemmy-instances.csv" target="_blank" download>awesome-lemmy-instances.csv</a> file

> ⓘ Note To view a wider version of the table, [click here](README.md).
'''

csv_contents = "Instance,NU,NC,Fed,Adult,↓V,Users\n"

################
# PROCESS JSON #
################

import os
print( os.path.dirname(os.path.realpath(__file__)) )
print( os.getcwd() )
print( os.listdir() )
print( os.listdir('lemmy-stats-crawler') )

with open( LEMMY_STATS_CRAWLER_FILEPATH ) as json_data:
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
		federated_linked = None
		federated_allowed = None
		federated_blocked = None

	registration_mode = instance['site_info']['site_view']['local_site']['registration_mode']
	slur_filter = instance['site_info']['site_view']['local_site']['slur_filter_regex']
	community_creation_admin_only = instance['site_info']['site_view']['local_site']['community_creation_admin_only']
	enable_downvotes = instance['site_info']['site_view']['local_site']['enable_downvotes']
	enable_nsfw = instance['site_info']['site_view']['local_site']['enable_nsfw']
	users_month = instance['site_info']['site_view']['counts']['users_active_month']
	registration_mode = instance['site_info']['site_view']['local_site']['registration_mode']

	#print( instance['site_info']['site_view'] )

	# is this instance adult-friendly?
	if slur_filter != None or enable_nsfw != True:
		adult = 'No'
	else:
		adult = 'Yes'

	if community_creation_admin_only == True:
		new_comm = "No"
	else:
		new_comm = "Yes"

	if federation_enabled == False or federated_allowed != None:
		fed = 'No'
	else:
		fed = "Yes"

	if enable_downvotes == True:
		downvotes = "Yes"
	else:
		downvotes = "No"

	if registration_mode == "closed":
		new_users = "No"
	else:
		new_users = "Yes"

	csv_contents += "[" +name+ "](https://" +domain+ "),"
	csv_contents += new_users+ ","
	csv_contents += new_comm+ ","
	csv_contents += fed+ ","
	csv_contents += adult+ ","
	csv_contents += downvotes+ ","
	csv_contents += str(users_month)
	csv_contents += "\n"

# write the instance data table to the csv file
with open( "awesome-lemmy-instances.csv", "w" ) as csv_file:
	csv_file.write( csv_contents )

# convert csv file data to markdown table
df = pd.read_csv( "awesome-lemmy-instances.csv" )
markdown_table = df.to_markdown( tablefmt='pipe', index = False )

# add newline to protect the table from getting klobbered by the text around it
markdown_table = "\n" + markdown_table + "\n"

# add the markdown table to the readme's contents
readme_contents += markdown_table

readme_contents +=  """
# What's next?

## Subscribe to ~~Subreddits~~ Communities

After you pick an instance and register an account, you'll want to subscribe to communities. You can subscribe to "local" communities on your instance, and (if you chose an instance that isn't siloed) you can also subscribe to "remote" communities on other instances.

To **find popular communities** across all lemmy instances in the fediverse, you can use the [Lemmy Community Browser](https://browse.feddit.de/) run by feddit.de.

 * https://browse.feddit.de/

## Other links

You may want to also checkout the following websites for more information about Lemmy

 * [Official Lemmy Documentation](https://join-lemmy.org/docs/en/index.html)
 * [Lemmy Map](https://lemmymap.feddit.de) - Data visualization of lemmy instances
 * [The Federation Info](https://the-federation.info/platform/73) - Another table comparing lemmy instances (with pretty charts)
 * [Federation Observer](https://lemmy.fediverse.observer/list) - Yet another table comparing lemmy instances
 * [FediDB](https://fedidb.org/software/lemmy) - Yet another site comparing lemmy instances (with pretty charts)
 * [Lemmy Sourcecode](https://github.com/LemmyNet/lemmy)
 * [Jerboa (Official Android Client)](https://f-droid.org/packages/com.jerboa/)
 * [Mlem (iOS Client)](https://testflight.apple.com/join/xQfmkJhc)

"""

with open( "README.md", "w" ) as readme_file:
	readme_file.write( readme_contents )
