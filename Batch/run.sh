#!/bin/bash

echo "  *******************************  importing batch table  *******************************"

export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH


startDate=$(date -u '+%Y-%m-%d %H:00:00' -d "-24hour")
endDate=$(date -u '+%Y-%m-%d %H:00:00' -d "-1hour")
echo "start date: ${startDate}"
echo "end date: ${endDate}"


python3 Batch/batch_indexer.py "${startDate}" "${endDate}" 
rc=$?; if [[ $rc != 0 ]]; then 
    echo "problem with batch indexer. Exiting."
    exit $rc
fi

echo "Indexing DONE"