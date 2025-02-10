import os
import sys
import cx_Oracle
import sender

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

sel = 'SELECT MONTH, YEAR, NMEMBERS, CPUTIME, WALLTIME, NJOBS, NCORES, INSERTED_DATE FROM ATLAS_LOCALGROUPDISK_MGT.USATLASLXBATCH'
sel += " WHERE INSERTED_DATE >= TO_DATE( :start_date, 'YYYY-MM-DD HH24:MI:SS')"
sel += " AND INSERTED_DATE < TO_DATE( :end_date, 'YYYY-MM-DD HH24:MI:SS') "

# print(sel)

cursor.execute(sel, start_date=start_date, end_date=end_date)

data = []
count = 0
for row in cursor:
    doc={
        'end_time': str(row[1])+"-"+str(row[0])+"-05T00:00:00",
        'usid': [f"u_{i}" for i in range(row[2])]
    }
    # doc['inserted_time'] = str(row[2]).replace(' ', 'T')
    data.append(doc)
    print(row)

sender.send_condorjob(data)
print('condorjob docs:', len(data))


sel = 'SELECT RECORDDATE, NMEMBERS, INSERTED_DATE FROM ATLAS_LOCALGROUPDISK_MGT.USATLASLXPLUS'
sel += " WHERE RECORDDATE >= TO_DATE( :start_date, 'YYYY-MM-DD HH24:MI:SS')"
sel += " AND RECORDDATE < TO_DATE( :end_date, 'YYYY-MM-DD HH24:MI:SS') "

# print(sel)

cursor.execute(sel, start_date=start_date, end_date=end_date)

data = []
count = 0
for row in cursor:
    doc={
        'end_time': str(row[0]).replace(' ', 'T'),
        'nusers': row[1],
        'users': [f"u_{i}" for i in range(row[1])]
    }
    data.append(doc)
    print(row)

sender.send_ssh(data)
print('ssh docs:', len(data))