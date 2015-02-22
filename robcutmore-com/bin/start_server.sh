#!/bin/bash

cd /home/rc/projects/robcutmore
myenv/bin/gunicorn -c robcutmore-com/config/gunicorn.py mysite.wsgi