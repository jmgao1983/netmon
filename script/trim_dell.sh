#!/bin/sh
cp routesum rtsum
cat route|awk 'NR>12{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5}' > route.tmp
mv -f route.tmp route
