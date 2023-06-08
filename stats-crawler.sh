#!/bin/sh
set -x

#####################
# DECLARE VARIABLES #
#####################

# get the current branch of the 'awesome-lemmy-instances' repo
current_branch=$(git branch --show-current)

crawl_list="baraza.africa,lemmy.ml,beehaw.org,lemmygrad.ml,feddit.de,lemmy.blahaj.zone"

#############
# FUNCTIONS #
#############

FATAL() {
	printf 'FATAL: %s. Aborting.\n' "$*"
	exit 1
}

#######################
# LEMMY-STATS-CRAWLER #
#######################

# this is so fucking unsafe https://rustup.rs/
#curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
which cargo
cargo --version

{ git clone https://github.com/LemmyNet/lemmy-stats-crawler.git \
&& cd lemmy-stats-crawler; } || FATAL 'Git clone failed';

# some pre-run output for debugging
ls

# is this our dev branch?
if [ "${current_branch}" = "dev" ]; then
	# this is a run in dev; We limit the `max-crawl-distance` to 0 here (so
	# the crawler does not go to other instances than those explicitly
	# listed), for faster execution.

	time cargo run -- --start-instances $crawl_list \
	--json --max-crawl-distance 0 > lemmy-stats-crawler.json

else
	# this isn't dev; do a full crawl

	time cargo run -- --start-instances $crawl_list \
	--json > lemmy-stats-crawler.json

fi

# some post-run output for debugging
ls
du -sh lemmy-stats-crawler.json
wc -l lemmy-stats-crawler.json
head lemmy-stats-crawler.json
tail lemmy-stats-crawler.json

exit 0
