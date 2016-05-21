#!/bin/sh
sed -i '/ $/{
N
s/ \r\n      / /}' route.txt
cat route.txt | grep 'via' | awk '{print $3 "\t" $6}' | grep -v '\[' > route.tmp
cat route.txt | grep 'via' | awk '{print $2 "\t" $5}' | grep -v 'via' >> route.tmp
cat route.tmp | sort -g > route
rm -f route.tmp
cat routesum | grep -v 'internal' | awk 'NR>4{printf"%-15s%-15s%-15s%-15s\n",$1,$2,$3,$4}' > rtsum
sed -i '1,6d' conf
