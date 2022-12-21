import requests
import pandas as pd
import os
import sys

# suppress InsecureRequestWarning: Unverified HTTPS request is being made.
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(ROOT_DIR, '..')


def enhance_queues():

    url_queue_all = 'https://atlas-cric.cern.ch/api/atlas/site/query/?json&pandaqueue_state=ANY'
    try:
        r = requests.get(url_queue_all, verify=False)
        cric_queues = r.json()

        enhanced_queues = []
        for queue, attrs in cric_queues.items():
            print(queue, attrs)
            queues_dict = {
                'queue': queue,
                'site': attrs['rc_site'],
                'cloud': attrs['cloud'],
                'tier_level': attrs['tier_level'],
                'cric_status': attrs['status'],
                'cric_state': attrs['state'],
                'cric_resource_type': attrs['resource_type'],
                'nodes': attrs['nodes'],
                'corepower': attrs['corepower'],
                'corecount': attrs['corecount'],
                'region': attrs['region']
            }

            enhanced_queues.append(queues_dict)

        enhanced_queues = pd.DataFrame(enhanced_queues)

        return enhanced_queues

    except:
        print("Could not get sites from CRIC. Exiting...")
        print("Unexpected error: ", str(sys.exc_info()[0]))
