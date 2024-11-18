#!/bin/bash
DB_FILE_PATH="/usr/src/app/instance"
BACKUP_FOLDER=/opt/backup
TIMESTAMP=$(date +"%Y%m%d%H%M%S")
BACKUP_FILE="db_backup_$TIMESTAMP.sqlite3"

mkdir -p $BACKUP_FOLDER
docker run --rm --volumes-from apeaj-web -v $BACKUP_FOLDER:/backup alpine sh -c "cp $DB_FILE_PATH/project.db /backup/$BACKUP_FILE"

BACKUP_COUNT=$(ls -1 $BACKUP_FOLDER | wc -l)
if [ $BACKUP_COUNT -gt 5 ]; then
    ls -t $BACKUP_FOLDER | tail -n +6 | xargs -I {} rm -f $BACKUP_FOLDER/{}
fi