#!/bin/bash
set -x

#####################
# DECLARE VARIABLES #
#####################

# get the current branch of the 'awesome-lemmy-instances' repo
current_branch=$(git branch --show-current)

crawl_list="baraza.africa,lemmygrad.ml,lemmy.blahaj.zone,lemmy.pussthecat.org,lemmy.studio,toast.ooo,iusearchlinux.fyi,waveform.social,monero.town,exploding-heads.com,reddthat.com,mander.xyz,vlemmy.net,szmer.info"

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

CARGO=$(which cargo)
if [[ -z ${CARGO} ]]; then
	CARGO="${HOME}/.cargo/bin/cargo"
fi
${CARGO} --version

git clone https://github.com/LemmyNet/lemmy-stats-crawler.git
pushd lemmy-stats-crawler

# some pre-run output for debugging
ls

# is this our dev branch?
if [ "${current_branch}" = "dev" ]; then
	# this is a run in dev; We limit the `max-crawl-distance` to 0 here (so
	# the crawler does not go to other instances than those explicitly
	# listed), for faster execution.

	time ${CARGO} run -- --start-instances $crawl_list \
	--json --max-crawl-distance 0 > lemmy-stats-crawler.json

else
	# this isn't dev; do a full crawl

	time ${CARGO} run -- --start-instances $crawl_list \
	--json > lemmy-stats-crawler.json

fi

# some post-run output for debugging
ls
du -sh lemmy-stats-crawler.json
wc -l lemmy-stats-crawler.json
head lemmy-stats-crawler.json
tail lemmy-stats-crawler.json

exit 0
