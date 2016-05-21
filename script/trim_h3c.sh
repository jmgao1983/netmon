#!/bin/sh
cp route.txt route
sed -i '1,6d' route
cat routesum|awk '{print $1 "\t" $2 "\t" $3}' > rtsum
