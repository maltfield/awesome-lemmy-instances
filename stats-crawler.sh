#!/bin/bash
set -x

# this is so fucking unsafe https://rustup.rs/
#curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
which cargo
cargo --version

git clone https://github.com/LemmyNet/lemmy-stats-crawler.git
cd lemmy-stats-crawler

#~/.cargo/bin/cargo run -- --start-instances baraza.africa,lemmy.ml
ls

# is this our dev branch?
current_branch=$(git branch --show-current)
if [[ "${current_branch}" == "dev" ]]; then
	# this is a run in dev; keep the list short for faster iteration

	time cargo run -- --start-instances baraza.africa,lemmy.ml,beehaw.org,lemmygrad.ml,feddit.de --json --max-crawl-distance 0 > lemmy-stats-crawler.json

else
	# this isn't dev; do a full crawl

	time cargo run -- --start-instances baraza.africa,lemmy.ml,beehaw.org,lemmygrad.ml,feddit.de --json > lemmy-stats-crawler.json

fi

ls
du -sh lemmy-stats-crawler.json
wc -l lemmy-stats-crawler.json
head lemmy-stats-crawler.json
tail lemmy-stats-crawler.json

exit 0
