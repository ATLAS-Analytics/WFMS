import os
import sys
import cx_Oracle
import estools

if 'JOB_ORACLE_CONNECTION_STRING' not in os.environ:
    print('Connection to ORACLE DB not configured. Please set variable: JOB_ORACLE_CONNECTION_STRING ')
    sys.exit(-1)

if 'JOB_ORACLE_PASS' not in os.environ or 'JOB_ORACLE_USER' not in os.environ:
    print('Please set variables:JOB_ORACLE_USER and JOB_ORACLE_PASS.')
    sys.exit(-1)

if not len(sys.argv) == 3:
    print('Please provide Start and End times in YYYY-mm-DD HH:MM::SS format.')
    sys.exit(-1)

start_date = sys.argv[1]
end_date = sys.argv[2]

print('Start date:', start_date, '\t End date:', end_date)

user = os.environ['JOB_ORACLE_USER']
passw = os.environ['JOB_ORACLE_PASS']
conn = os.environ['JOB_ORACLE_CONNECTION_STRING'].replace('jdbc:oracle:thin:@//', '')
con = cx_Oracle.connect(user + '/' + passw + '@' + conn)
print(con.version)

cursor = con.cursor()

columns = [
    'JEDITASKID', 'TASKNAME', 'STATUS', 'USERNAME', 'REQID', 'OLDSTATUS', 'CLOUD', 'SITE', 'PRODSOURCELABEL', 'WORKINGGROUP',
    'VO', 'CORECOUNT', 'TASKTYPE', 'PROCESSINGTYPE', 'TASKPRIORITY', 'CURRENTPRIORITY', 'ARCHITECTURE', 'TRANSUSES',
    'TRANSHOME', 'TRANSPATH', 'LOCKEDBY', 'TERMCONDITION', 'SPLITRULE', 'WALLTIME', 'WALLTIMEUNIT', 'OUTDISKCOUNT',
    'OUTDISKUNIT', 'WORKDISKCOUNT', 'WORKDISKUNIT', 'RAMCOUNT', 'RAMUNIT', 'IOINTENSITY', 'IOINTENSITYUNIT',
    'WORKQUEUE_ID', 'PROGRESS', 'FAILURERATE', 'ERRORDIALOG', 'COUNTRYGROUP', 'PARENT_TID', 'EVENTSERVICE',
    'TICKETID', 'TICKETSYSTEMTYPE', 'SUPERSTATUS', 'CAMPAIGN', 'MERGERAMCOUNT', 'MERGERAMUNIT', 'MERGEWALLTIME',
    'MERGEWALLTIMEUNIT', 'NUMTHROTTLED', 'MERGECORECOUNT', 'GOAL', 'CPUTIME', 'CPUTIMEUNIT', 'CPUEFFICIENCY',
    'BASEWALLTIME', 'AMIFLAG_OLD', 'AMIFLAG', 'NUCLEUS', 'BASERAMCOUNT', 'LOCKEDTIME', 'STATECHANGETIME', 'THROTTLEDTIME',
    'ASSESSMENTTIME', 'CREATIONDATE', 'MODIFICATIONTIME', 'STARTTIME', 'ENDTIME', 'FROZENTIME',
    'TTCREQUESTED', 'TTCPREDICTED', 'TTCPREDICTIONDATE', 'RESCUETIME', 'REQUESTTYPE', 'GSHARE', 'USEJUMBO',
    'RESOURCE_TYPE', 'DISKIO', 'DISKIOUNIT', 'ATTEMPTNR'
]

escolumns = [
    'jeditaskid', 'taskname', 'status', 'username', 'reqid', 'oldstatus', 'cloud', 'site', 'prodsourcelabel', 'workinggroup',
    'vo', 'corecount',  'tasktype',  'processingtype', 'taskpriority', 'currentpriority', 'architecture',  'transuses',
    'transhome', 'transpath', 'lockedby', 'termcondition', 'splitrule', 'walltime', 'walltimeunit', 'outdiskcount',
    'outdiskunit', 'workdiskcount', 'workdiskunit', 'ramcount', 'ramunit', 'iointensity', 'iointensityunit',
    'workqueue_id', 'progress', 'failurerate', 'errordialog', 'countrygroup', 'parent_tid', 'eventservice',
    'ticketid', 'ticketsystemtype', 'superstatus', 'campaign', 'mergeramcount', 'mergeramunit', 'mergewalltime',
    'mergewalltimeunit', 'numthrottled', 'mergecorecount', 'goal', 'cputime', 'cputimeunit', 'cpuefficiency',
    'basewalltime', 'amiflag_old', 'amiflag', 'nucleus', 'baseramcount', 'lockedtime', 'statechangetime', 'throttledtime',
    'assessmenttime', 'creationdate', 'modificationtime', 'starttime', 'endtime', 'frozentime',
    'ttcrequested',  'ttcpredicted', 'ttcpredictiondate', 'rescuetime', 'requesttype',  'gshare',  'usejumbo',
    'resource_type', 'diskio',  'diskiounit', 'attemptnr'
]

sel = 'SELECT '
sel += ','.join(columns)
sel += ' FROM ATLAS_PANDA.JEDI_TASKS'
# sel += ' WHERE JEDITASKID=123'
sel += " WHERE MODIFICATIONTIME >= TO_DATE( :start_date, 'YYYY-MM-DD HH24:MI:SS')"
sel += " AND MODIFICATIONTIME < TO_DATE( :end_date, 'YYYY-MM-DD HH24:MI:SS')"

# print(sel)

cursor.execute(sel, start_date=start_date, end_date=end_date)


es = estools.get_es_connection()

data = []
count = 0
for row in cursor:
    doc = {}
    for colName, colValue in zip(escolumns, row):
        # print(colName, colValue)
        doc[colName] = colValue

    if doc['lockedtime']:
        doc['lockedtime'] = str(doc['lockedtime']).replace(' ', 'T')
    if doc['statechangetime']:
        doc['statechangetime'] = str(doc['statechangetime']).replace(' ', 'T')
    if doc['creationdate']:
        doc['creationdate'] = str(doc['creationdate']).replace(' ', 'T')
    if doc['modificationtime']:
        doc['modificationtime'] = str(doc['modificationtime']).replace(' ', 'T')
    if doc['starttime']:
        doc['starttime'] = str(doc['starttime']).replace(' ', 'T')
    if doc['endtime']:
        doc['endtime'] = str(doc['endtime']).replace(' ', 'T')
    if doc['frozentime']:
        doc['frozentime'] = str(doc['frozentime']).replace(' ', 'T')
    if doc['rescuetime']:
        doc['rescuetime'] = str(doc['rescuetime']).replace(' ', 'T')
    if doc['ttcpredictiondate']:
        doc['ttcpredictiondate'] = str(doc['ttcpredictiondate']).replace(' ', 'T')

    doc["_index"] = "tasks_archive_" + doc['creationdate'].split('-')[0]
    doc["_id"] = doc['jeditaskid']

    data.append(doc)
    # print(doc)

    if not count % 500:
        print(count)
        res = estools.bulk_index(data, es)
        if res:
            del data[:]
    count += 1

estools.bulk_index(data, es)
print('final count:', count)


con.close()
