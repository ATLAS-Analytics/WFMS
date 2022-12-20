import urllib.parse
import requests
import pandas as pd
import configparser
import os
from datetime import datetime
import ssl
import urllib3
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, '..' )

http = urllib3.PoolManager(
    cert_file="SSL_CERT",
    cert_reqs="CERT_REQUIRED",
    key_file="SSL_KEY",
    key_password="CERT_PWD",
    ca_certs="CERT_CERT")
)

def enhance_queues(all=False, with_rse=False):

    url_queue_all = 'https://atlas-cric.cern.ch/api/atlas/site/query/?json&pandaqueue_state=ANY'
    url_queue = 'https://atlas-cric.cern.ch/api/atlas/pandaqueue/query/?json'
    response = http.request('GET',url_queue_all if all else url_queue)
    data = response.data
    cric_queues = json.loads(data)
    enhanced_queues = []

    for queue, attrs in cric_queues.items():
        queues_dict = {
            'queue': queue,
            'site': attrs['rc_site'],
            'cloud': attrs['cloud'],
            'tier_level': attrs['tier_level'],
            'transferring_limit': attrs['transferringlimit'] or 2000,
            'status': attrs['status'],
            'state': attrs['state'],
            'resource_type': attrs['resource_type'],
            'nodes': attrs['nodes'],
            'corepower': attrs['corepower'],
            'corecount': attrs['corecount'],
            'region': attrs['region']
        }

        if with_rse:
            datadisks = [[d for d in v if 'DATADISK' in d or 'VP_DISK' in d] for k, v in attrs['astorages'].items()]
            flat_datadisks = list(set([item for sublist in datadisks for item in sublist]))
            queues_dict['rse'] = flat_datadisks or 'no rse'

        enhanced_queues.append(queues_dict)

    enhanced_queues = pd.DataFrame(enhanced_queues)

    return enhanced_queues.explode('rse') if with_rse else enhanced_queues

