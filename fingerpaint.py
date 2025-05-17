#!/usr/bin/python3
'''
Author: Ethan Ashley
This is used by draw.sh to use fingerpaint to turn the touchpad into a drawing pad.
'''

import re
import sys
from fingerpaint.fingerpaint import cli
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(cli())

# https://pypi.org/project/fingerpaint/

