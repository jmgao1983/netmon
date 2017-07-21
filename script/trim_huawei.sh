#!/bin/sh
sed -i '/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/d' conf
cat int|awk 'NR>2{print $1 "\t" $2 "\t" $3}' > int2
mv -f int2 int
sed -i '/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/d' mod
sed -i '/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/d' route
cat routesum|awk 'NR>2{print $1 "\t" $2 "\t" $3}' > rtsum
sed -i '/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}/d' stp
