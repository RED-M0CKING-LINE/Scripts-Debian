#!/bin/bash

# This script will delete the token balance and trust chain of Tribler installed via Flatpak.
# This is because the token balance system is broken, and it will continue to go negative while purely uploading, so a positive balance is near impossible.
# This can increase download and upload speeds because you will not be seen as a selfish user by the network, though it may take time for you to rebuild the databse of potential routes
# https://www.tribler.org/

#HOME=  # Define this variable if $HOME is not already a system variable
tribler_folder="$HOME/.var/app/org.tribler.Tribler/.Tribler"
version_folder="$(/usr/bin/ls -vd $tribler_folder/*/ | /usr/bin/tail -n 1)"  # This uses ls to derive the highest versioned folder in this directory

/usr/bin/trash "$version_folder/sqlite/bandwidth - BACKUP.db"
/usr/bin/mv "$version_folder/sqlite/bandwidth.db" "$version_folder/sqlite/bandwidth - BACKUP.db"
 
