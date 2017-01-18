#!/bin/bash

set -e

HOME_DIR=/home/test
BACKUP_DIR=/data/fuiou_upload_backup

[ ! -d "$BACKUP_DIR" ] && mkdir -p $BACKUP_DIR

cd $HOME_DIR
for i in $(ls *.zip);do
lftp ftp://username:password@host:port <<EOF
mput *.zip
bye
EOF
break
done 2> /dev/null

mv $HOME_DIR/*.zip $BACKUP_DIR -f 2> /dev/null