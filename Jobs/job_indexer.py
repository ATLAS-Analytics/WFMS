import os
import sys
import cx_Oracle
import estools
import conversions

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

user = os.environ['JOB_ORACLE_USER']
passw = os.environ['JOB_ORACLE_PASS']
conn = os.environ['JOB_ORACLE_CONNECTION_STRING'].replace('jdbc:oracle:thin:@//', '')
con = cx_Oracle.connect(user + '/' + passw + '@' + conn)
# con = cx_Oracle.connect(user + '/' + passw + '@adcr_prodsys')
print(con.version)


cursor = con.cursor()
not_stored_anymore = ['MAXCPUUNIT', 'MAXDISKUNIT',
                      'IPCONNECTIVITY', 'MINRAMUNIT', 'PRODDBUPDATETIME', 'NINPUTFILES']
print('omitting columns:', not_stored_anymore)


columns = [
    'JOBS.PANDAID', 'JOBS.JOBDEFINITIONID', 'JOBS.SCHEDULERID', 'JOBS.PILOTID', 'JOBS.CREATIONTIME', 'JOBS.CREATIONHOST', 'JOBS.MODIFICATIONTIME',
    'JOBS.MODIFICATIONHOST', 'JOBS.ATLASRELEASE', 'JOBS.TRANSFORMATION', 'JOBS.HOMEPACKAGE', 'JOBS.PRODSERIESLABEL', 'JOBS.PRODSOURCELABEL',
    'JOBS.PRODUSERID', 'JOBS.ASSIGNEDPRIORITY', 'JOBS.CURRENTPRIORITY', 'JOBS.ATTEMPTNR', 'JOBS.MAXATTEMPT', 'JOBS.JOBSTATUS', 'JOBS.JOBNAME',
    'JOBS.MAXCPUCOUNT', 'JOBS.MAXDISKCOUNT', 'JOBS.MINRAMCOUNT',
    'JOBS.STARTTIME', 'JOBS.ENDTIME', 'JOBS.CPUCONSUMPTIONTIME', 'JOBS.CPUCONSUMPTIONUNIT', 'JOBS.COMMANDTOPILOT', 'JOBS.TRANSEXITCODE',
    'JOBS.PILOTERRORCODE', 'JOBS.PILOTERRORDIAG', 'JOBS.EXEERRORCODE', 'JOBS.EXEERRORDIAG', 'JOBS.SUPERRORCODE', 'JOBS.SUPERRORDIAG',
    'JOBS.DDMERRORCODE', 'JOBS.DDMERRORDIAG', 'JOBS.BROKERAGEERRORCODE', 'JOBS.BROKERAGEERRORDIAG', 'JOBS.JOBDISPATCHERERRORCODE',
    'JOBS.JOBDISPATCHERERRORDIAG', 'JOBS.TASKBUFFERERRORCODE', 'JOBS.TASKBUFFERERRORDIAG', 'JOBS.COMPUTINGSITE', 'JOBS.COMPUTINGELEMENT',
    'JOBS.PRODDBLOCK', 'JOBS.DISPATCHDBLOCK', 'JOBS.DESTINATIONDBLOCK', 'JOBS.DESTINATIONSE', 'JOBS.NEVENTS', 'JOBS.GRID', 'JOBS.CLOUD', 'JOBS.CPUCONVERSION',
    'JOBS.SOURCESITE', 'JOBS.DESTINATIONSITE', 'JOBS.TRANSFERTYPE', 'JOBS.TASKID', 'JOBS.CMTCONFIG', 'JOBS.STATECHANGETIME',
    'JOBS.LOCKEDBY', 'JOBS.RELOCATIONFLAG', 'JOBS.JOBEXECUTIONID', 'JOBS.VO', 'JOBS.WORKINGGROUP', 'JOBS.PROCESSINGTYPE', 'JOBS.PRODUSERNAME',
    'JOBS.COUNTRYGROUP', 'JOBS.BATCHID', 'JOBS.PARENTID', 'JOBS.SPECIALHANDLING', 'JOBS.JOBSETID', 'JOBS.CORECOUNT', 'JOBS.NINPUTDATAFILES',
    'JOBS.INPUTFILETYPE', 'JOBS.INPUTFILEPROJECT', 'JOBS.INPUTFILEBYTES', 'JOBS.NOUTPUTDATAFILES', 'JOBS.OUTPUTFILEBYTES', 'JOBS.JOBMETRICS',
    'JOBS.WORKQUEUE_ID', 'JOBS.JEDITASKID', 'JOBS.JOBSUBSTATUS', 'JOBS.ACTUALCORECOUNT', 'JOBS.REQID', 'JOBS.MAXRSS', 'JOBS.MAXVMEM', 'JOBS.MAXPSS',
    'JOBS.AVGRSS', 'JOBS.AVGVMEM', 'JOBS.AVGSWAP', 'JOBS.AVGPSS', 'JOBS.MAXWALLTIME', 'JOBS.NUCLEUS', 'JOBS.EVENTSERVICE', 'JOBS.FAILEDATTEMPT', 'JOBS.HS06SEC', 'JOBS.HS06', 'JOBS.GSHARE',
    'JOBS.TOTRCHAR', 'JOBS.TOTWCHAR', 'JOBS.TOTRBYTES', 'JOBS.TOTWBYTES', 'JOBS.RATERCHAR', 'JOBS.RATEWCHAR', 'JOBS.RATERBYTES', 'JOBS.RATEWBYTES',
    'JOBS.PILOTTIMING', 'JOBS.MEMORY_LEAK', 'JOBS.RESOURCE_TYPE', 'JOBS.DISKIO', 'JOBS.CONTAINER_NAME', 'TASKS.SIMULATION_TYPE'
]

escolumns = [
    'pandaid', 'jobdefinitionid', 'schedulerid', 'pilotid', 'creationtime', 'creationhost', 'modificationtime',
    'modificationhost', 'atlasrelease', 'transformation', 'homepackage', 'prodserieslabel', 'prodsourcelabel',
    'produserid', 'assignedpriority', 'currentpriority', 'attemptnr', 'maxattempt', 'jobstatus', 'jobname',
    'maxcpucount', 'maxdiskcount', 'minramcount',
    'starttime', 'endtime', 'cpuconsumptiontime', 'cpuconsumptionunit', 'commandtopilot', 'transexitcode',
    'piloterrorcode', 'piloterrordiag', 'exeerrorcode', 'exeerrordiag', 'superrorcode', 'superrordiag',
    'ddmerrorcode', 'ddmerrordiag', 'brokerageerrorcode', 'brokerageerrordiag', 'jobdispatchererrorcode',
    'jobdispatchererrordiag', 'taskbuffererrorcode', 'taskbuffererrordiag', 'computingsite', 'computingelement',
    'proddblock', 'dispatchdblock', 'destinationdblock', 'destinationse', 'nevents', 'grid', 'cloud', 'cpuconversion',
    'sourcesite', 'destinationsite', 'transfertype', 'taskid', 'cmtconfig', 'statechangetime',
    'lockedby', 'relocationflag', 'jobexecutionid', 'vo', 'workinggroup', 'processingtype', 'produsername',
    'countrygroup', 'batchid', 'parentid', 'specialhandling', 'jobsetid', 'corecount', 'ninputdatafiles',
    'inputfiletype', 'inputfileproject', 'inputfilebytes', 'noutputdatafiles', 'outputfilebytes', 'jobmetrics',
    'workqueue_id', 'jeditaskid', 'jobsubstatus', 'actualcorecount', 'reqid', 'maxrss', 'maxvmem', 'maxpss',
    'avgrss', 'avgvmem', 'avgswap', 'avgpss', 'maxwalltime', 'nucleus', 'eventservice', 'failedattempt', 'hs06sec', 'hs06', 'gShare',
    'IOcharRead', 'IOcharWritten', 'IObytesRead', 'IObytesWritten', 'IOcharReadRate', 'IOcharWriteRate', 'IObytesReadRate', 'IObytesWriteRate',
    'pilottiming', 'memory_leak', 'resource_type', 'diskio', 'container_name', 'simulation_type'
]

sel = 'SELECT '
sel += ','.join(columns)
sel += ' FROM ATLAS_PANDA.JOBSARCHIVED4 JOBS LEFT JOIN ATLAS_DEFT.T_PRODUCTION_TASK TASKS'
sel += ' ON JOBS.JEDITASKID = TASKS.TASKID'
# sel += ' AND PANDAID=4225560422'
# sel += ' AND ROWNUM < 3'
sel += " WHERE JOBS.STATECHANGETIME >= TO_DATE( :start_date, 'YYYY-MM-DD HH24:MI:SS')"
sel += " AND JOBS.STATECHANGETIME < TO_DATE( :end_date, 'YYYY-MM-DD HH24:MI:SS') "

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

    if doc['creationtime']:
        doc['creationtime'] = str(doc['creationtime']).replace(' ', 'T')
    if doc['modificationtime']:
        doc['modificationtime'] = str(
            doc['modificationtime']).replace(' ', 'T')
    if doc['starttime']:
        doc['starttime'] = str(doc['starttime']).replace(' ', 'T')
    if doc['endtime']:
        doc['endtime'] = str(doc['endtime']).replace(' ', 'T')
    doc['cpuconsumptiontime'] = int(doc['cpuconsumptiontime'])
    if doc['statechangetime']:
        doc['statechangetime'] = str(doc['statechangetime']).replace(' ', 'T')

    (doc['dbTime'], doc['dbData'], doc['workDirSize'], doc['jobmetrics']) = conversions.splitJobmetrics(doc['jobmetrics'])
    (doc['wall_time'], doc['cpu_eff'], doc['queue_time']) = conversions.deriveDurationAndCPUeff( doc['creationtime'], doc['starttime'], doc['endtime'], doc['cpuconsumptiontime'])
    
    dts = conversions.deriveTimes(doc['pilottiming'])
    if len(dts) == 5:
        (doc['timeGetJob'], doc['timeStageIn'], doc['timeExe'], doc['timeStageOut'], doc['timeSetup']) = dts
    
    if len(dts) == 6:
        (doc['timeGetJob'], doc['timeStageIn'], doc['timeExe'], doc['timeStageOut'], doc['time_initial_setup'], doc['time_payload_setup'] ) = dts
    
    doc["_index"] = "jobs_archive_write"
    doc["_id"] = doc['pandaid']

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
