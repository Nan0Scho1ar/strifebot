#!/bin/bash
echo "============================================" \
	 > >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' >&2)
echo "Strifebot Startup Script Initialised" \
	 > >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' >&2)
cd $(dirname "$0")
cd ../strifebot/
echo "Starting Strifebot" \
	> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' >&2)
python3.9 ./bot.py strife.conf \
	> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 } fflush()' >&2)
echo "Stopped Strifebot" \
	 > >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }') \
	2> >(gawk '{ print strftime("[%Y-%m-%d %H:%M:%S]"), $0 }' >&2)
