#!/usr/bin/bash
# This deletes all Flatpak Chromium data except for Bookmarks

#rm -rfv ~/.var/app/org.chromium.Chromium/
find ~/.var/app/org.chromium.Chromium/* ! -name 'Bookmarks' -delete -print
