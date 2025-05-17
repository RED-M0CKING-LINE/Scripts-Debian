#!/bin/bash

# This is the script i use to update my system
# There is a WIP version which uses tmux to run these different tasks in parallel

SUDO='' && [[ $EUID -ne 0 ]] && SUDO='/usr/bin/sudo' && /usr/bin/echo "Authorizing Use Of SUDO Privilages..." && sudo /usr/bin/echo -n

/usr/bin/echo -e "\n\n===== APT UPDATE ====="
$SUDO /usr/bin/apt update

/usr/bin/echo -e "\n\n===== APT UPGRADABLE ====="
/usr/bin/apt list --upgradable

/usr/bin/echo -e "\n\n===== APT-FAST DOWNLOAD ====="
$SUDO /usr/bin/apt-fast upgrade --download-only --assume-yes | grep -v " Download complete: " | grep -v " Verification finished successfully. " | grep -vx "\[DL:.+\]" | grep -vE "^(\n)?$"

/usr/bin/echo -e "\n\n===== CHKBOOT CHECK ====="
$SUDO /usr/bin/chkboot

/usr/bin/echo -e "\n\n\a===== APT UPGRADE ====="
$SUDO /usr/bin/apt upgrade

/usr/bin/echo -e "\n\n\a===== APT AUTOREMOVE ====="
$SUDO /usr/bin/apt autoremove --purge

/usr/bin/echo -e "\n\n===== FLATPAK UPDATE ====="
/usr/bin/flatpak update --assumeyes

/usr/bin/echo -e "\n\n===== FLATPAK AUTOREMOVE ====="
/usr/bin/flatpak uninstall --unused

/usr/bin/echo -e "\n\n===== FIRMWARE UPDATES ====="
/usr/bin/fwupdmgr get-updates
#$SUDO /usr/bin/fwupdmgr update

/usr/bin/echo -e "\n\n\a===== COMPLETE ====="
