#!/bin/bash

# Signs the modules for VBOX and VMWare with the MOK
# Generate the MOK with update-secureboot-policy --new-key

SUDO='' && [[ $EUID -ne 0 ]] && SUDO='sudo'  # Ensure the user is a superuser. This is great for scripts in the user path (~/.local/bin or ~/bin)

# To find which modules need to be signed, use `dmesg`
# To use with other modules, simply edit the following list: (Should look something like `module_list=(vmmon vmnet)`
module_list=(vmnet vmmon vboxdrv vboxnetflt vboxnetadp vboxpci)
#module_list=(vboxdrv vboxnetflt vboxnetadp vboxpci)

echo "Module List: ${module_list[@]}"

echo "Signing Modules..."
for m in $($SUDO modinfo -n "${module_list[@]}")
do
echo $m
$SUDO /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 /var/lib/shim-signed/mok/MOK.priv /var/lib/shim-signed/mok/MOK.der $m
done

echo "Loading Modules..."
$SUDO /usr/sbin/modprobe -v -a "${module_list[@]}"

echo "Done."
