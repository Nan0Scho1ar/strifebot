#!/bin/bash
echo "Database Startup Script Initialised" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
cd $(dirname "$0")
cd ../database/
echo "Sending Notifications" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
curl -X POST https://maker.ifttt.com/trigger/Nameless_Database_Starting/with/key/cD0bTvh4VLLT3wHpy-X2mg > /dev/null 2>/dev/null
echo "Notifications Sent" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
echo "Starting Database" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
python3.9 ./topicREST.py \
	> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()' >&2)
echo "Stopped Database" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
