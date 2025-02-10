import requests


def send_condorjob(data):
    # reformat things
    ndata = []
    for doc in data:
        ndoc = {
            'token': 'cern2diduhGJHV',
            'kind': 'condorjob',
            'cluster': 'CERN',
            'state': 'finished',
            'users': doc['usid'],
            # 'Id': doc['_id'].split("#")[1],
            # 'Runtime': doc['duration'],
            'timestamp': f"{doc['end_time'][:23]}Z"
        }
        print(ndoc)
        ndata.append(ndoc)
    resp = requests.post('https://af.atlas-ml.org/', json=ndata)
    print(f'sender resp:{resp}')

def send_ssh(data):
    # reformat things
    ndata = []
    for doc in data:
        ndoc = {
            'token': 'cern2diduhGJHV',
            'kind': 'ssh',
            'cluster': 'CERN',
            'ssh_user_count': doc['nusers'],
            'users': doc['users'],
            'timestamp': f"{doc['end_time'][:23]}Z"
        }
        print(ndoc)
        ndata.append(ndoc)
    resp = requests.post('https://af.atlas-ml.org/', json=ndata)
    print(f'sender resp:{resp}')
