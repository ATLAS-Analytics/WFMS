import requests


def send(data):
    # reformat things
    ndata = []
    for doc in data:
        ndoc = {
            'kind': 'condorjob',
            'cluster': 'lxbatch',
            'state': 'finished',
            'users': doc['usid'],
            'Id': 'xxx',
            'Runtime': doc['duration'],
            '_id': doc['_id'],
            '@timestamp': doc['end_time']
        }
        ndata.append(ndoc)
    resp = requests.post('https://af.atlas-ml.org/', json=ndata)
    print(f'sender resp:{resp}')

# example doc
# "_id": "UC-AF-emsmith-648384.154",
# "kind": "condorjob",
# "cluster": "UC-AF",
# "state": "finished",
# "users": "emsmith",
# "Id": "648384.154",
# "@timestamp": "2023-10-10T23:08:32.243736065Z",
# "Runtime": 790
