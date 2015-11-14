#!/usr/bin/env bash
echo "Enter database user for robcutmore.com project: "
read db_user
pg_dump \
    --host=localhost \
    --username="$db_user" \
    --dbname=robcutmore_com \
    --file=robcutmore.sql
