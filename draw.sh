#!/bin/bash
# Depends on fingerpaint: https://pypi.org/project/fingerpaint/
# install finger paint as user: $ pip3 install --user fingerpaint
# currently broken because fingerpaint is not available through the package manager and you cannot install python packages system-wide
# Depends on ./fingerpaint.py

# Turns the touchpad into a drawing pad

fingerpaint.py --dark --width 1200 --hint=$'Press any key or click to finish drawing\nImage will be copied to clipboard' --output - | wl-copy --type image/png

