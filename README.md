# proxmox_fan_controller
Systems supporting ipmitool can utilize these tools

Do you find your proxmox server noisy?

This approach has worked for me, and without buying new expensive quiet fans this will make your home-lab server quiet.

This has been tested on the Supermicro AS -E301-9D-8CN4 with Proxmox 8.3.3 (as of Jan 2025)
 
## Requirements:
- Proxmox 
- ipmitool

## The approach

This approach relies of direct communication with the management interface to set fan speed. and it sets it on boot, and I setup a script to react to temperature change to avoid blowing it up.

