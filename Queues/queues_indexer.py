import os
import sys
import cx_Oracle
import estools
import pandas as pd
from cric_json_api import enhance_queues

if 'JOB_ORACLE_CONNECTION_STRING' not in os.environ:
    print('Connection to ORACLE DB not configured. Please set variable: JOB_ORACLE_CONNECTION_STRING ')
    sys.exit(-1)

if 'JOB_ORACLE_PASS' not in os.environ or 'JOB_ORACLE_USER' not in os.environ:
    print('Please set variables:JOB_ORACLE_USER and JOB_ORACLE_PASS.')
    sys.exit(-1)

if not len(sys.argv) == 3:
    print('Pleae provide Start and End times in YYYY-mm-DD HH:MM::SS format.')
    sys.exit(-1)

start_date = sys.argv[1]
end_date = sys.argv[2]

print('Start date:', start_date, '\tEnd date:', end_date)


from_cric = enhance_queues()

user = os.environ['JOB_ORACLE_USER']
passw = os.environ['JOB_ORACLE_PASS']
conn = os.environ['JOB_ORACLE_CONNECTION_STRING'].replace('jdbc:oracle:thin:@//', '')
con = cx_Oracle.connect(user + '/' + passw + '@' + conn)
print(con.version)


cursor = con.cursor()

columns = [
    'START_TIME',
    'END_TIME',
    'PANDAID',
    'QUEUE',
    'GSHARE',
    'PRODUSERNAME',
    'TRANSFORMATION',
    'RESOURCE_TYPE',
    'STATUS',
    'FINAL_STATUS',
    'INPUTFILEBYTES',
    'OUTPUTFILEBYTES',
    'DURATION',
    'CPUCONSUMPTIONUNIT',
    'PRODDBLOCK',
    'PROCESSINGTYPE',
    'INPUTFILETYPE',
    'INPUTFILEPROJECT'
]

escolumns = [
    'start_time',
    'end_time',
    'pandaid',
    'queue',
    'gshare',
    'produsername',
    'transformation',
    'resource_type',
    'status',
    'final_status',
    'inputfilebytes',
    'outputfilebytes',
    'duration',
    'cpuconsumptionunit',
    'proddblock',
    'processingtype',
    'inputfiletype',
    'inputfileproject'
]

with open('/home/analyticssvc/Queues/queues_jobs_workload.sql') as fp:
    sel = ''.join(fp.readlines())
    print(sel)

    cursor.execute(sel, start_date=start_date, end_date=end_date)

    es = estools.get_es_connection()

    data = []
    count = 0
    for row in cursor:
        doc = {}
        for colName, colValue in zip(escolumns, row):
            # print(colName, colValue)
            doc[colName] = colValue

        if doc['start_time']:
            doc['start_time'] = str(
                doc['start_time']).replace(' ', 'T')
        if doc['end_time']:
            doc['end_time'] = str(doc['end_time']).replace(' ', 'T')

        doc["_index"] = "queue"

        data.append(doc)
        # print(doc)

        if not count % 500:
            print(count)
            data_df = pd.DataFrame(data)
            print(data_df.columns)
            result = pd.merge(data_df, from_cric, left_on='queue', right_on='queue')
            data = data_df.to_dict(orient='records')
            res = estools.bulk_index(data, es)
            if res:
                del data[:]
        count += 1

    estools.bulk_index(data, es)
    print('final count:', count)


con.close()
