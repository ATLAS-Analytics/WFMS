#!/bin/bash
# accepts only one parameter: date that has to be fixed. 
# eg. fix.sh 2018-01-01
echo "  *******************************  fixing tasks   *******************************"

export LD_LIBRARY_PATH=/opt/oracle/instantclient_21_1:$LD_LIBRARY_PATH

startDate="$1 00:00:00"
endDate="$1 23:59:59"

echo "start date: ${startDate}"
echo "end date: ${endDate}"


python3 task_indexer.py "${startDate}" "${endDate}" 
rc=$?; if [[ $rc != 0 ]]; then 
    echo "problem with job indexer. Exiting."
    exit $rc
fi

echo "Indexing UC DONE."