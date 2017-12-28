#!/bin/bash

set -e

#DATE=$(date +%Y-%m-%d)
#LOG_DIR=publish_log
#LOG_FILE=$LOG_DIR/${DATE}_publish.log

#[ ! -d "$LOG_DIR" ] && mkdir -p ./$LOG_DIR

cd /root/gogo_build/gogo/

git pull > /dev/null 2>&1
echo "pull code success"

mvn clean package -Ptest > /dev/null 2>&1
echo "compile and package success"

PID=$(ps aux | grep /opt/tomcat-gogo-api | grep -v grep | awk '{print $2}')

if [ -n "$PID" ];then
    kill $PID
    echo "stop service success"
else
    echo "service not running"
fi

sleep 2
rm -rf /opt/tomcat-gogo-api/webapps/*
cp /root/gogo_build/gogo/gogo-api/target/gogoapi.war /opt/tomcat-gogo-api/webapps/
/opt/tomcat-gogo-api/bin/startup.sh
echo "start service success"
