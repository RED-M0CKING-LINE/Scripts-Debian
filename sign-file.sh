#!/bin/bash

# A convinence script to put the sign-file command into the path for the current kernel
# sign-file is a script for signing kernel modules for linux

exec /usr/src/linux-headers-$(uname -r)/scripts/sign-file sha256 /var/lib/shim-signed/mok/MOK.priv /var/lib/shim-signed/mok/MOK.der $@

# you may be looking for the kernel_module-sign-VMs.sh to sign VMWare or VBOX modules automagically

