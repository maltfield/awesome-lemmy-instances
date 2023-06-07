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
time cargo run -- --start-instances baraza.africa,lemmy.ml,beehaw.org,lemmygrad.ml,feddit.de --json > lemmy-stats-crawler.json
ls
du -sh lemmy-stats-crawler.json
wc -l lemmy-stats-crawler.json
head lemmy-stats-crawler.json
tail lemmy-stats-crawler.json

exit 0
