from datetime import datetime
import time


def strToTS(d):
    (dat, tim) = d.split(' ')
    (Y, M, D) = dat.split('-')
    (h, m, s) = tim.split(':')
    t = datetime(int(Y), int(M), int(D), int(h), int(m), int(float(s)))
    return t


@outputSchema('tuple( timeGetJob:int, timeStageIn:int, timeExe:int, timeStageOut:int, timeSetup:int)')
def deriveTimes(origString):
    if origString is None:
        return (0, 0, 0, 0, 0)
    times = origString.split('|')
    if len(times) == 4:
        times.append(0)
    return (int(float(times[0])), int(float(times[1])), int(float(times[2])), int(float(times[3])), int(float(times[4])))


@outputSchema('tuple( dbTime:float, dbData:int, workDirSize:int, rest:chararray )')
def splitJobmetrics(origString):
    if origString is None:
        return (0, 0, 0, None)
    parts = origString.split(' ')
    rest = ''
    dbTime = None
    dbData = None
    workDirSize = None
    for p in parts:
        if not '=' in p:
            rest += p + ' '
            continue
        k, v = p.split('=')
        if k == 'coreCount' or k == 'nEvents':
            continue
        if k == 'dbTime':
            dbTime = float(v)
            continue
        if k == 'dbData':
            dbData = int(v)
            continue
        if k == 'workDirSize':
            workDirSize = int(v)
            continue
        rest += p + ' '
    rest = rest.strip()
    if len(rest) == 0:
        rest = None
    return (dbTime, dbData, workDirSize, rest)


@outputSchema('tuple( walltime:int, cpueff:float, queue_time:int)')
def deriveDurationAndCPUeff(CREATIONTIME, STARTTIME, ENDTIME, CPUCONSUMPTIONTIME):
    if CREATIONTIME is None or STARTTIME is None or ENDTIME is None or CPUCONSUMPTIONTIME is None:
        return (0, 0.0, 0)
    CREATIONTIME = CREATIONTIME / 1000
    STARTTIME = STARTTIME / 1000
    ENDTIME = ENDTIME / 1000

    walltime = ENDTIME - STARTTIME
    queue_time = STARTTIME - CREATIONTIME

    cpueff = 0
    try:
        if walltime > 0 and CPUCONSUMPTIONTIME != '':
            cpueff = float(CPUCONSUMPTIONTIME) / walltime
    except:
        print "problem with cpueff: " + CPUCONSUMPTIONTIME

    return (walltime, cpueff, queue_time)


@outputSchema('tuple( walltime:int, cpueff:float, queue_time:int)')
def deriveDurationAndCPUeffNEW(CREATIONTIME, STARTTIME, ENDTIME, CPUCONSUMPTIONTIME):
    if CREATIONTIME is None or STARTTIME is None or ENDTIME is None or CPUCONSUMPTIONTIME is None:
        return (0, 0.0, 0)
    CREATIONTIME = strToTS(CREATIONTIME)
    STARTTIME = strToTS(STARTTIME)
    ENDTIME = strToTS(ENDTIME)

    wt = ENDTIME - STARTTIME
    qt = STARTTIME - CREATIONTIME
    walltime = wt.seconds + wt.days * 86400
    queue_time = qt.seconds + qt.days * 86400

    cpueff = 0
    try:
        if walltime > 0 and CPUCONSUMPTIONTIME != '':
            cpueff = float(CPUCONSUMPTIONTIME) / walltime
    except:
        print "problem with cpueff: " + CPUCONSUMPTIONTIME

    return (walltime, cpueff, queue_time)


@outputSchema('TIMESTAMP:chararray')
def Tstamp(ts):
    if ts is None:
        return(0)
    else:
        return(datetime.fromtimestamp(ts / 1000).isoformat())


@outputSchema('TIMESTAMP:chararray')
def TstampNEW(ts):
    if ts is None:
        return(0)
    else:
        d = strToTS(ts)
        return(int(1000 * time.mktime(d.timetuple())))
