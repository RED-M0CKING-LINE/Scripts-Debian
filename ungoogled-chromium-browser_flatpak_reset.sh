#!/usr/bin/bash
# This deletes all Flatpak Ungoogled Chromium data except for Bookmarks

#rm -rfv ~/.var/app/com.github.Eloston.UngoogledChromium
find ~/.var/app/com.github.Eloston.UngoogledChromium/* ! -name 'Bookmarks' -delete -print
