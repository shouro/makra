#!/usr/bin/env bash

source /home/shouro/ws/makra/minispider/venv/bin/activate
cd /home/shouro/ws/makra/minispider
YDATE=$(date -d "yesterday 13:00" '+%Y-%m-%d')
LOGDATE=$(date -d "yesterday 13:00" '+%Y_%m_%d')
scrapy crawl paloarchive -a startdate=$YDATE -a enddate=$YDATE --logfile=/home/shouro/ws/logs/palo_${LOGDATE}.log -s JOBDIR=/home/shouro/ws/jobs/palo_${LOGDATE}
