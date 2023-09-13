import os
import sys
import cx_Oracle
import estools
# import conversions

if 'JOB_ORACLE_CONNECTION_STRING' not in os.environ:
    print('Connection to ORACLE DB not configured. Please set variable: JOB_ORACLE_CONNECTION_STRING ')
    sys.exit(-1)

if 'BATCH_ORACLE_PASS' not in os.environ or 'BATCH_ORACLE_USER' not in os.environ:
    print('Please set variables:BATCH_ORACLE_USER and BATCH_ORACLE_PASS.')
    sys.exit(-1)

if not len(sys.argv) == 3:
    print('Pleae provide Start and End times in YYYY-mm-DD HH:MM::SS format.')
    sys.exit(-1)

start_date = sys.argv[1]
end_date = sys.argv[2]

print('Start date:', start_date, '\tEnd date:', end_date)

user = os.environ['BATCH_ORACLE_USER']
passw = os.environ['BATCH_ORACLE_PASS']
conn = os.environ['JOB_ORACLE_CONNECTION_STRING'].replace('jdbc:oracle:thin:@//', '')
con = cx_Oracle.connect(user + '/' + passw + '@' + conn)
# con = cx_Oracle.connect(user + '/' + passw + '@adcr_prodsys')
print(con.version)


cursor = con.cursor()

sel = 'SELECT DISTINCT ACCOUNTINGGROUP '
sel += ' FROM ATLAS_LOCALGROUPDISK_MGT.LOCALJOBSCERNCONDOR'
sel += " WHERE JOBS.STATECHANGETIME >= TO_DATE( :start_date, 'YYYY-MM-DD HH24:MI:SS')"
sel += " AND JOBS.STATECHANGETIME < TO_DATE( :end_date, 'YYYY-MM-DD HH24:MI:SS') "

# print(sel)

cursor.execute(sel, start_date=start_date, end_date=end_date)

es = estools.get_es_connection()

data = []
count = 0
for row in cursor:
    doc = {}

    # for colName, colValue in zip(escolumns, row):
    #     # print(colName, colValue)
    #     doc[colName] = colValue

    # if doc['creationtime']:
    #     doc['creationtime'] = str(doc['creationtime']).replace(' ', 'T')
    # if doc['modificationtime']:
    #     doc['modificationtime'] = str(
    #         doc['modificationtime']).replace(' ', 'T')
    # if doc['starttime']:
    #     doc['starttime'] = str(doc['starttime']).replace(' ', 'T')
    # if doc['endtime']:
    #     doc['endtime'] = str(doc['endtime']).replace(' ', 'T')

    # doc["_index"] = "batch_archive_write"
    # doc["_id"] = doc['pandaid']

    data.append(doc)
    print(row)

    if not count % 500:
        print(count)
        # res = estools.bulk_index(data, es)
        # if res:
        # del data[:]
    count += 1

# estools.bulk_index(data, es)
print('final count:', count)

con.close()
