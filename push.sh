#!/bin/sh
# Purpose: a stupid git wrapper to deal with conflicts of ephemeral files
#          when we push to GitHub
git pull
git checkout --theirs README.md
git checkout --theirs awesome-lemmy-instances.csv
git push
