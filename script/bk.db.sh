#!/bin/sh
cd /var/www/html/netmon/db
mv -f netmon.sql netmon.sql.bk.1
mysqldump -unetmon -pnetmon --databases netmon > netmon.sql
