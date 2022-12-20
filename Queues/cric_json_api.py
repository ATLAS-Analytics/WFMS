import requests
import pandas as pd
import os
import sys

# suppress InsecureRequestWarning: Unverified HTTPS request is being made.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, '..')


def enhance_queues(all=False, with_rse=False):

    url_queue_all = 'https://atlas-cric.cern.ch/api/atlas/site/query/?json&pandaqueue_state=ANY'
    url_queue = 'https://atlas-cric.cern.ch/api/atlas/pandaqueue/query/?json'
    try:
        r = requests.get(url_queue_all if all else url_queue, verify=False)
        cric_queues = r.json()
        # print('whole json:', cric_queues)

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
                datadisks = [[d for d in v if 'DATADISK' in d or 'VP_DISK' in d]
                             for k, v in attrs['astorages'].items()]
                flat_datadisks = list(set([item for sublist in datadisks for item in sublist]))
                queues_dict['rse'] = flat_datadisks or 'no rse'

            enhanced_queues.append(queues_dict)

        enhanced_queues = pd.DataFrame(enhanced_queues)

        return enhanced_queues.explode('rse') if with_rse else enhanced_queues

    except:
        print("Could not get sites from CRIC. Exiting...")
        print("Unexpected error: ", str(sys.exc_info()[0]))
