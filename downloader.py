# handles downloads

import urllib.request
import os
import time

def download(url, path, retries=3):
    for attempt in range(retries):
        try:
            urllib.request.urlretrieve(url, path)
            if os.path.getsize(path) > 0:
                return True
        except:
            time.sleep(1)
    return False
