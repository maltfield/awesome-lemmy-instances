#!/usr/bin/env python3
################################################################################
# File:    generate_readme.py
# Version: 0.5
# Purpose: Creates the README.md file for this repo
# Authors: Michael Altfield <michael@michaelaltfield.net>
# Created: 2023-06-06
# Updated: 2024-05-06
################################################################################

################################################################################
#                                   IMPORTS                                    #
################################################################################

import json, csv, numpy, datetime, warnings
import pandas as pd

################################################################################
#                                  SETTINGS                                    #
################################################################################

LEMMY_STATS_CRAWLER_FILENAME = 'lemmy-stats-crawler.json'
LEMMY_STATS_CRAWLER_FILEPATH = 'lemmy-stats-crawler/' + LEMMY_STATS_CRAWLER_FILENAME

UPTIME_FILENAME = 'uptime.json'
AGE_FILENAME = 'age.json'

OUT_CSV = 'awesome-lemmy-instances.csv'

################################################################################
#                                  FUNCTIONS                                   #
################################################################################

# do some checks on text that we get back from the instance's API because it
# might break markdown or do something nasty
def sanitize_text( text ):

	# markdown table columns are delimited by pipes
	text = text.replace( '|', '' )

	# newlines
	text = text.replace( "\r", '' )
	text = text.replace( "\n", '' )

	# commas fuck with our CSV file; replace it with this homoglyph (0x201A)
	text = text.replace( ",", '‚' )

	return text

################################################################################
#                                  MAIN BODY                                   #
################################################################################

# catch runtime warnings from numpy on 'nan' errors when calculating averages
warnings.filterwarnings("error")

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
'''

csv_contents = "Instance,NU,NC,Fed,Adult,↓V,Users,BI,BB,UT,MO,Version\n"

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

#print( "data:|" +str(data)+ "|" )

instances_with_blocked = [x for x in data['instance_details'] if x['federated_instances']['federated_instances']['blocked'] != [] ]

with open( UPTIME_FILENAME ) as json_data:
	uptime_data = json.load(json_data)

with open( AGE_FILENAME ) as json_data:
	age_data = json.load(json_data)

for instance in data['instance_details']:

	domain = sanitize_text( instance['domain'] )
	name = sanitize_text( instance['site_info']['site_view']['site']['name'] )
	version = sanitize_text( instance['site_info']['version'] )
	federation_enabled = instance['site_info']['site_view']['local_site']['federation_enabled']

	print( domain )
	print( "\tversion:|" +str(version)+ "|" )

	if federation_enabled == True:
#		print( "\tfederated_instances:|" +str(instance['federated_instances'].keys())+ "|" )
#		print( "\tfederated_instances.federated_instances:|" +str(instance['federated_instances']['federated_instances'].keys())+ "|" )
#		print( "\tsite_info.site_view.local_site:|" +str(instance['site_info']['site_view']['local_site'].keys())+ "|" )

		federated_linked = instance['federated_instances']['federated_instances']['linked']
		federated_allowed = instance['federated_instances']['federated_instances']['allowed']
		federated_blocked = instance['federated_instances']['federated_instances']['blocked']
	else:
		federated_linked = None
		federated_allowed = None
		federated_blocked = None

	registration_mode = instance['site_info']['site_view']['local_site']['registration_mode']

	if 'slur_filter' in instance['site_info']['site_view']['local_site'].keys():
		slur_filter = instance['site_info']['site_view']['local_site']['slur_filter_regex']
	else:
		slur_filter = None

	community_creation_admin_only = instance['site_info']['site_view']['local_site']['community_creation_admin_only']
	enable_downvotes = instance['site_info']['site_view']['local_site']['enable_downvotes']
	enable_nsfw = instance['site_info']['site_view']['local_site']['enable_nsfw']
	users_month = instance['site_info']['site_view']['counts']['users_active_month']
	registration_mode = instance['site_info']['site_view']['local_site']['registration_mode']

	# count the number of instances that block this instance
	blocked_by = 0
	for i in instances_with_blocked:
		for item in i['federated_instances']['federated_instances']['blocked']:
			if item['domain'] == domain:
				blocked_by += 1

	# count the number of instances that this instance blocks
	if instance['federated_instances'] == None:
		blocking = 0
	elif instance['federated_instances']['federated_instances']['blocked'] == None:
		blocking = 0
	else:
		blocking = len(instance['federated_instances']['federated_instances']['blocked'])

	print( "\tblocked_by:|" +str(blocked_by)+ "|" )
	print( "\tblocking:|" +str(blocking)+ "|" )

	# is this instance adult-friendly?
	if slur_filter != None or enable_nsfw != True:
		adult = 'No'
	else:
		adult = 'Yes'

	if community_creation_admin_only == True:
		new_comm = "No"
	else:
		new_comm = "Yes"

	if federation_enabled == False or federated_allowed != []:
		fed = 'No'
	else:
		fed = "Yes"
	print( "\tfederation_enabled:|" +str(federation_enabled)+ "|" )
	print( "\tfederated_allowed:|" +str(federated_allowed)+ "|" )
	print( "\tfed:|" +str(fed)+ "|" )

	if enable_downvotes == True:
		downvotes = "Yes"
	else:
		downvotes = "No"

	if registration_mode == "closed":
		new_users = "No"
	else:
		new_users = "Yes"

	# stupid way to say gimmie the 'uptime_alltime' data from the json where
	# the 'domain' matches this iteration lemmy instance's domain
	uptime = [x['uptime_alltime'] for x in uptime_data['data']['nodes'] if x['domain'] == domain]

	# stupid way to say gimmie the 'monthsmonitored' data from the json where
	# the 'domain' matches this iteration lemmy instance's domain
	age = [x['monthsmonitored'] for x in age_data['data']['nodes'] if x['domain'] == domain]

	# did we figure out an uptime for this domain?
	if uptime == []:
		# we couldn't find an uptime; set it to '??'
		uptime = '??'
	else:
		# we got an uptime! Format it for the table

		uptime = uptime[0]
		# let's keep the data simple
		uptime = round(float(uptime))
		uptime = str(uptime)+ "%"

	# did we figure out an age for this domain?
	if age == []:
		# we couldn't find an uptime; set it to '??'
		age = '??'
	else:
		# we got an uptime! Format it for the table

		age = age[0]
		# let's keep the data simple
		age = round(float(age))

	csv_contents += "[" +name+ "](https://" +domain+ "),"
	csv_contents += new_users+ ","
	csv_contents += new_comm+ ","
	csv_contents += fed+ ","
	csv_contents += adult+ ","
	csv_contents += downvotes+ ","
	csv_contents += str(users_month)+ ','
	csv_contents += str(blocking)+ ','
	csv_contents += str(blocked_by)+ ','
	csv_contents += str(uptime)+ ','
	csv_contents += str(age)+ ','
	csv_contents += version
	csv_contents += "\n"

# write the instance data table to the csv file
with open( OUT_CSV, "w" ) as csv_file:
	csv_file.write( csv_contents )

#########################
# RECOMMENDED INSTANCES #
#########################

# shrink the list to just a few recommended instances
all_instances = list()
recommended_instances = list()
with open(OUT_CSV) as csv_file:

	for instance in csv.DictReader( csv_file ):
		all_instances.append( instance )

		# only include instances that are "yes" across-the-board
		if instance['NU'] == "Yes" \
		 and instance['NC'] == "Yes" \
		 and instance['Fed'] == "Yes" \
		 and instance['Adult'] == "Yes" \
		 and instance['↓V'] == "Yes":

			recommended_instances.append( instance )

# remove instances with too few or too may users
recommended_instances = [x for x in recommended_instances if int(x['Users']) > 60 and int(x['Users']) < 1000]

# get a lits of all the instances that have more than 1 blocked instance and
# then get the average number of instances that are blocked
try:
	bi_list = [ int(x['BI']) for x in all_instances if int(x['BI']) > 1 ]
	bi_avg = numpy.average( bi_list )
except (Exception, RuntimeWarning) as e:
	print( "WARNING: Caught numpy exception when calculating bi_avg: " +str(e) )
	bi_avg = 2

# get a lits of all the instances that are blocked by more than 1 instance and
# then get the average number of that instances are are blocked
try:
	bb_list = [ int(x['BB']) for x in all_instances if int(x['BB']) > 1 ]
	bb_avg = numpy.average( bb_list )
except (Exception, RuntimeWarning) as e:
	print( "WARNING: Caught numpy exception when calculating bb_avg: " +str(e) )
	bb_avg = 2

print( "bi_avg:|" +str(bi_avg)+ "|" )
print( "bb_avg:|" +str(bb_avg)+ "|" )

# remove instances that are blocking or blocked-by too many other instancesk
recommended_instances = [ x for x in recommended_instances if int(x['BI']) <= bi_avg and int(x['BB']) <= bb_avg ]

# remove instances that haven't been online for 2 months
recommended_instances = [ x for x in recommended_instances if int(x['MO']) >= 2 ]

# limit to those with the best uptime; first we make sure that we actually
# have the uptime data
uptime_available = [x for x in recommended_instances if x['UT'] != '??']

# do we have uptime data?
if uptime_available != list():
	# we have uptime data; proceed with reducing the set of recommended_instances
	# based on uptime

	# loop down from 100% to 0%
	for percent_uptime in reversed(range(100)):

		high_uptime_instances = [x for x in recommended_instances if x['UT'] != '??' and int(x['UT'][:-1]) > percent_uptime]

		# do we have more than one instance above this uptime?
		if len(high_uptime_instances) > 1:
			# we already have enough instances; ignore the rest with lower uptime
			recommended_instances = high_uptime_instances
			break

# prepare data for csv file
csv_contents = "Instance,NU,NC,Fed,Adult,↓V,Users,BI,BB,UT,MO,Version\n"
for instance in recommended_instances:
	csv_contents += instance['Instance']+ ','
	csv_contents += instance['NU']+ ','
	csv_contents += instance['NC']+ ','
	csv_contents += instance['Fed']+ ','
	csv_contents += instance['Adult']+ ','
	csv_contents += instance['↓V']+ ','
	csv_contents += instance['Users']+ ','
	csv_contents += instance['BI']+ ','
	csv_contents += instance['BB']+ ','
	csv_contents += instance['UT']+ ','
	csv_contents += instance['MO']+ ','
	csv_contents += instance['Version']
	csv_contents += "\n"

# write the recommended instance data table to a csv file
with open( 'recommended-instances.csv', "w" ) as csv_file:
	csv_file.write( csv_contents )

# convert csv file data to markdown table
df = pd.read_csv( 'recommended-instances.csv' )
recommended_markdown_table = df.to_markdown( tablefmt='pipe', index = False )

# add newline to protect the table from getting klobbered by the text around it
recommended_markdown_table = "\n" + recommended_markdown_table + "\n"

readme_contents +=  """
# Recommended Instances

Just **click on a random instance** from the below "recommended" instances.

Don't overthink this. **It doesn't matter which instance you use.** You'll still be able to interact with communities (subreddits) on all other instances, regardless of which instance your account lives 🙂
"""

# add the markdown table to the readme's contents
readme_contents += recommended_markdown_table

# add more info
readme_contents +=  """
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
 * **BI** The number of instances that this instance is completely **BlockIng**. If this number is high, then users on this instance will be limited in what they can see on the lemmyverse.
 * **BB** The number of instances that this instances is completely **Blocked By**. If this number is high, then users on this instance will be limited in what they can see on the lemmyverse.
 * **UT** Percent **UpTime** that the server has been online
 * **MO** Number of **Months Online** since this server was first discovered. Higher is better.
 * **Version** The version of Lemmy this instance is running.

# What's next?

## Subscribe to ~~Subreddits~~ Communities

After you pick an instance and register an account, you'll want to subscribe to communities. You can subscribe to "local" communities on your instance, and (if you chose an instance that isn't siloed) you can also subscribe to "remote" communities on other instances.

To **find popular communities** across all lemmy instances in the fediverse, you can use the [Lemmy Community Browser](https://browse.feddit.de/) run by feddit.de.

 * https://browse.feddit.de/

If you want a more direct mapping of your favorite /r/subreddits to lemmy, checkout these sites:

1. [redditmigration.com](https://redditmigration.com/)
1. [sub.rehab](https://sub.rehab/?searchTerm=&visibleServices=lemmy&officialOnly=false&newOnly=false&favoriteOnly=false&sortBy=users_active_week)
1. yoasif's [Unofficial Subreddit Migration List](https://www.quippd.com/writing/2023/06/15/unofficial-subreddit-migration-list-lemmy-kbin-etc.html)


<a href="https://tech.michaelaltfield.net/2023/06/11/lemmy-migration-find-subreddits-communities/"><img src="lemmy-migration-find-subreddits-communities.jpg" alt="How To Find Lemmy Communities" /></a>

For more information, see my guide on [How to Find Popular Lemmy Communities](https://tech.michaelaltfield.net/2023/06/11/lemmy-migration-find-subreddits-communities/)

## Other links

You may want to also checkout the following websites for more information about Lemmy

 * [Official Lemmy Documentation](https://join-lemmy.org/docs/en/index.html)
 * [Intro to Lemmy Guide](https://tech.michaelaltfield.net/2023/06/11/lemmy-migration-find-subreddits-communities/) - How to create a lemmy account, find, and subscribe-to popular communities
 * [Lemmy Community Browser](https://browse.feddit.de/) - List of all communities across all lemmy instances, sorted by popularity
 * [Lemmy Map](https://lemmymap.feddit.de) - Data visualization of lemmy instances
 * [The Federation Info](https://the-federation.info/platform/73) - Another table comparing lemmy instances (with pretty charts)
 * [Federation Observer](https://lemmy.fediverse.observer/list) - Yet another table comparing lemmy instances
 * [FediDB](https://fedidb.org/software/lemmy) - Yet another site comparing lemmy instances (with pretty charts)
 * [Lemmy Sourcecode](https://github.com/LemmyNet/lemmy)
 * [Jerboa (Official Android Client)](https://f-droid.org/packages/com.jerboa/)
 * [Mlem (iOS Client)](https://apps.apple.com/gb/app/mlem-for-lemmy/id6450543782)

"""

#################
# ALL INSTANCES #
#################

# convert csv file data to markdown table
df = pd.read_csv( OUT_CSV )
markdown_table = df.to_markdown( tablefmt='pipe', index = False )

# add newline to protect the table from getting klobbered by the text around it
markdown_table = "\n" + markdown_table + "\n"

readme_contents +=  """
# All Lemmy Instances

Download table as <a href="https://raw.githubusercontent.com/maltfield/awesome-lemmy-instances/main/awesome-lemmy-instances.csv" target="_blank" download>awesome-lemmy-instances.csv</a> file

> ⓘ Note To view a wider version of the table, [click here](README.md).
"""

# add the markdown table to the readme's contents
readme_contents += markdown_table

timestamp = str(datetime.datetime.utcnow().isoformat())+ "+00:00"
readme_contents += "\n"
readme_contents += "Data generated at " +str(timestamp)
readme_contents += "\n"

with open( "README.md", "w" ) as readme_file:
	readme_file.write( readme_contents )
