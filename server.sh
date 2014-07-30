#!/bin/sh

PORT=9000

cd html
echo "open http://127.0.0.1:$PORT"
python2 -m SimpleHTTPServer $PORT 1>/dev/null 2>&1 &
