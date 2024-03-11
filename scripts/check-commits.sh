#!/bin/bash

errors=0
for commit in $(git rev-list $1)
do
    # check if command returns empty string
    # git show --format=format:%s%n%n%b%n --no-patch $commit | npm exec @commitlint/cli
    if [ -n "$(git show --format=format:%s%n%n%b%n --no-patch $commit | npm exec @commitlint/cli)" ]; then
        echo "Commit $commit is not following the commit message convention"
        # increment errors
        errors=$((errors+1))
    fi
done
# if there are errors, exit with status 1
if [ $errors -gt 0 ]; then
    exit 1
fi
