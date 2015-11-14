#!/usr/bin/env bash
project_dir=/home/rc/projects/robcutmore
gunicorn_location=$project_dir/env/bin/gunicorn
gunicorn_config=$project_dir/robcutmore-com/config/gunicorn.py
$gunicorn_location \
    --config=$gunicorn_config \
    mysite.wsgi
