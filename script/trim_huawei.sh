#!/bin/sh
sed -i '1,2d' conf
cat int|awk 'NR>2{print $1 "\t" $2 "\t" $3}' > int2
mv -f int2 int
sed -i '1,2d' mod
sed '1,2d' route.txt > route
cat routesum|awk 'NR>2{print $1 "\t" $2 "\t" $3}' > rtsum
sed -i '1,2d' stp
