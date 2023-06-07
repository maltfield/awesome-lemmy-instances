#!/bin/bash
set -x

# this is so fucking unsafe https://rustup.rs/
#curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
which cargo
cargo --version

git clone https://github.com/LemmyNet/lemmy-stats-crawler.git
cd lemmy-stats-crawler

#~/.cargo/bin/cargo run -- --start-instances baraza.africa,lemmy.ml
cargo run -- --start-instances baraza.africa,lemmy.ml,beehaw.org,lemmygrad.ml,feddit.de --json > lemmy-stats-crawler.json

exit 0
