#!/bin/bash
echo "Lavalink Startup Script Initialised" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
cd ../lavalink
echo "Sending Notifications" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
curl -X POST https://maker.ifttt.com/trigger/Lavalink_Starting/with/key/cD0bTvh4VLLT3wHpy-X2mg > /dev/null 2>/dev/null
echo "Notifications Sent" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
echo "Starting Lavalink" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
java -jar Lavalink.jar \
	> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()' >&2)
echo "Stopped Lavalink" 2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' 1>&2) | gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }'
