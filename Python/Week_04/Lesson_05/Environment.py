import os
from pprint import pprint
path = os.getenv('PATH')
if path:
    print(path)