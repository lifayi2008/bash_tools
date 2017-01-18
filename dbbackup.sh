#!/bin/bash

#set -e

MYSQLDUMP_BIN=/data/mysql/bin/mysqldump
BACKUP_DIR=/home/backup
DATE=$(date +%Y-%m-%d)
DATE_PRUNED=$(date +%Y-%m-%d --date="-1 month")

[ ! -d "$BACKUP_DIR" ] && mkdir -p $BACKUP_DIR

#arguments dbname host user password
backup_db() {
    DB_DIR=$BACKUP_DIR/$1
    [ ! -d "$DB_DIR" ] && mkdir -p $DB_DIR
    $MYSQLDUMP_BIN --set-gtid-purged=OFF -h$2 -u$3 -p$4 $1 > $DB_DIR/${1}-${DATE}.sql
    prune_files $1
}

prune_files() {
    PRUNE_FILE=${BACKUP_DIR}/${1}/${1}-${DATE_PRUNED}.sql
    [ -f $PRUNE_FILE ] && rm -f $PRUNE_FILE
}

#backup sbs
backup_db sbs 'host' root 'password'
backup_db sbs_wq 'host' root 'password'

#backup ebank007
backup_db zhangfu 'host' root 'password'
backup_db trades 'host' root 'password'

#backup pay_platform
backup_db unionpay 'host' root 'password'