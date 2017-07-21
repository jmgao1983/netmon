#!/bin/sh
sed -i -e '/^Brief/d' -e '/^Link/d' -e '/^Speed/d' -e '/^Type/d' -e '/^Proto/d' -e '/^$/d' int
sed -i '1,4d' route
cat routesum|awk 'NR>1{print $1 "\t" $2 "\t" $3}' > rtsum
