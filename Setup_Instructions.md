# Setup Instructions

Slightly ammended instructions from what is detailed by the GReX team [here](https://grex-telescope.github.io/software/server_setup/).

However I would recommend following that closely, this just details any workarounds I had to figure out for one reason or another, their website has many more details and explanations.

This was done on Ubuntu 24.04 LTS.

Sometimes you will need to reboot to apply updates you make.

Also, you should, of course have root priveliges to carry out these steps.

[File_structure.md](https://github.com/ismisebrendan/GReX_Birr_setup/blob/main/File_structure.md) details the necessary file structure for the server.

There are a few times where I mention to add lines to the ```.bashrc``` file in this document, [Lines_to_add_to_bashrc.md](https://github.com/ismisebrendan/GReX_Birr_setup/blob/main/Lines_to_add_to_bashrc.md) has all of these in the one place for ease.

## OS Setup
This ran without issues, you should be able to follow the steps outlined by the GReX team.

Update and upgrade the system.

```sh
sudo apt-get update
sudo apt-get upgrade -y
```

Set whatever hostname you want for the system, they do recommend naming machines ```grex-<affiliation>-<location>``` however.

```sh
sudo hostnamectl set-hostname <your-hostname>
```

Install some necessary programmes
```sh
sudo apt install net-tools
sudo apt install openssh-server
```

## Networking

Please note: To fully complete this part you must be connected to the GReX itself. However it is not necessary to complete this before you continue.

### Connecting to the GReX
There is a Raspberry Pi in the GReX box that you must connect to set up the SNAP board. You should be able to ssh to the pi as normal at the IP ```192.168.0.2```. Note, the instructions say that the username is ```pi``` however the username on the one we received was ```grex-pi``` so be sure to check that and the password on that account.

```sh
ssh grex-pi@192.168.0.2
```

You can set up ssh keypairs if you like also.

### Controlling the SNAP

This is detailed separately from the rest of the instructions [here](https://grex-telescope.github.io/software/operation/). To turn on/off the SNAP ssh to the Pi and create a bash script called ```snap.sh``` with the following contents

```sh
#!/bin/env bash
# Usage: ./snap.sh <on|off>
BASE_GPIO_PATH=/sys/class/gpio
PWN_PIN=20
if [ ! -e $BASE_GPIO_PATH/gpio$PWN_PIN ]; then
  echo "20" > $BASE_GPIO_PATH/export
fi
echo "out" > $BASE_GPIO_PATH/gpio$PWN_PIN/direction
if [[ -z $1 ]];
then
    echo "Please pass `on` or `off` as an argument"
else
    case $1 in
    "on" | "ON")
    echo "0" > $BASE_GPIO_PATH/gpio$PWN_PIN/value
    ;;
    "off" | "OFF")
    echo "1" > $BASE_GPIO_PATH/gpio$PWN_PIN/value
    ;;
    *)
    echo "Please pass `on` or `off` as an argument"
    exit -1
    ;;
    esac
fi
exit 0
```

Make it executable with

```sh
chmod +x snap.sh
```

Then run ```sudo ./snap.sh <on|off>``` to turn on and off the SNAP.

### Netplan

Remove all files from ```/etc/netplan```.

Chech which of NetworkManager or networkd is running - the desired situation is that networkd is running and NetworkManager is disabled.

```sh
systemctl status NetworkManager
systemctl status systemd-networkd
```

If NetworkManager is running and networkd is not NetworkManager must be disabled and networkd must be enabled using the below commands.

```sh
sudo systemctl stop NetworkManager
sudo systemctl disable NetworkManager
sudo systemctl enable systemd-networkd
```

Create the file ```/etc/netplan/config.yaml``` and add the following to it

```sh
network:
  version: 2
  renderer: networkd
  ethernets:
    # Two WAN interfaces. Configure this according to your network setup
    enp36s0f0:
      dhcp4: true
    enp36s0f1:
      dhcp4: true
    # 10 GbE connection over fiber to the box
    enp1s0f0:
      mtu: 9000
      addresses:
        - 192.168.0.1/24
        - 192.168.88.2/24
```

Then run
```sh
sudo netplan apply
```

We ran into warnings about permissions in this folder upon running the above command, so in order to set up the correct permissions for the config file run
```sh
sudo chmod go-rwx /etc/netplan/*
```

And then run 
```sh
sudo netplan apply
```
again.

Note: At one point after having moved the GPU in our computer the address of the fiber connection changed from ```enp1s0f0``` to ```enp2s0f0```. We are unsure why this happened, but simply changing any occurrences of ```enp1s0f0``` to ```enp2s0f0``` solves any issues you may encounter. 


### DHCP Server
Install the software
```sh
sudo apt-get install dnsmasq
```

Add the following lines to ```/etc/dnsmasq.conf``` if it exits, otherwise create it and add these lines to it (it was created already for me, but the installation instructions given tell you to create it).

```sh
# Only bind to the 10 GbE interface
interface=enp1s0f0
# Disable DNS
port=0
# DHCP Options
dhcp-range=192.168.0.0,static
dhcp-option=option:router,192.168.0.1
dhcp-option=option:netmask,255.255.255.0
#dhcp-host=<SNAP_MAC>,192.168.0.3,snap
log-async
log-queries
log-dhcp
```

Enable the DHCP server service
```sh
sudo systemctl enable dnsmasq --now
```

After this you must connect to the Pi and then the SNAP, but you can continute beyond this point and come back to it later without any issues, which is what we did.

Connect to the Pi and powercycle the SNAP as described above.

```sh
ssh grex-pi@192.168.0.2
```

```sh
sudo ./snap.sh off
```

```sh
sudo ./snap.sh on
```

Exit the pi and wait a few seconds. Open the ```dnsmasq``` log

```sh
journalctl -u dnsmasq
```

Skip to the bottom with Shift + G. There should be a line like the below visible

```sh
Jul 31 14:47:31 grex-tcd-birr dnsmasq-dhcp[9277]: 1481765933 DHCPDISCOVER(enp1s0f0) 00:10:5a:eb:15:12 no address available
```

This tells us that the SNAP has a MAC address of ```00:10:5a:eb:15:12``` (yours will be different). Exit the log with ```q``` and go back to ```/etc/dnsmasq.conf``` and uncomment the line ```#dhcp-host=<SNAP_MAC>,192.168.0.3,snap``` replacing ```<SNAP_MAC>``` with the MAC address of your SNAP.

Then restart the dhcp server with
```sh
sudo systemctl restart dnsmasq
```

After waiting for a little while you should now be able to ping the SNAP on ```192.168.0.3```

### Advanced 10 GbE settings
This ran without issues, you should be able to follow the steps outlined by the GReX team.

Create the file ```/etc/sysctl.d/20-grex.conf``` and add the following content to it
```sh
kernel.shmmax = 68719476736
kernel.shmall = 4294967296
net.core.rmem_max = 536870912
net.core.wmem_max = 536870912
net.core.optmem_max = 16777216
vm.swappiness=1
```

Apply these
```sh
sudo sysctl --system
```

Install another program
```sh
sudo apt-get install ethtool -y
```

Create the file ```/etc/rc.local``` and add the following content to it
```sh
#!/bin/env bash
ethtool -G enp1s0f0 rx 4096 tx 4096
ethtool -A enp1s0f0 rx on
ethtool -A enp1s0f0 tx on
```
Then make it executable
```sh
sudo chmod +x /etc/rc.local
```

Create the file ```/etc/systemd/system/rc-local.service``` and add the following content to it
```sh
[Unit]
 Description=/etc/rc.local Compatibility
 ConditionPathExists=/etc/rc.local

[Service]
 Type=forking
 ExecStart=/etc/rc.local start
 TimeoutSec=0
 StandardOutput=tty
 RemainAfterExit=yes
 SysVStartPriority=99

[Install]
 WantedBy=multi-user.target
```
Enable it
```sh
sudo systemctl enable rc-local
```
This requires a reboot.

## GPU drivers and CUDA
The recommended version of CUDA toolkit to install is 12.3, however this is not natively compatible with Ubuntu 24 and having this version caused issues down the line, as such we would recommend installing version 12.5 which was the most recent version at the time that we did this. It is entirely possible that htne newest version of CUDA toolkit whenever you're reading this works fine, or you may need to use another, older, version.

Installing CUDA toolkit.
```sh
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-5
```

Again, there were issues installing the specified versions of the drivers (545), we installed version 555 and had not problems because of this.
```sh
sudo apt-get install -y nvidia-kernel-open-555
sudo apt-get install -y cuda-drivers-555
```

The below command can be used to remove old dependencies and driver versions that might have come preinstalled.
```sh
sudo apt-get autoremove
```

Reboot, then run ```nvidia-smi``` to see if everyting is installed correctly. You should get something like this
```sh
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 555.42.06              Driver Version: 555.42.06      CUDA Version: 12.5     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 3090 Ti     Off |   00000000:41:00.0  On |                  Off |
|  0%   41C    P8             13W /  450W |     427MiB /  24564MiB |      6%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A      2659      G   /usr/lib/xorg/Xorg                             85MiB |
|    0   N/A  N/A      2990      G   /usr/bin/gnome-shell                           81MiB |
|    0   N/A  N/A      3859      G   ...irefox/4173/usr/lib/firefox/firefox          0MiB |
+-----------------------------------------------------------------------------------------+
```

To your ```~/.bashrc``` add
```sh
# CUDA 12.5
export PATH=/usr/local/cuda-12.5/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-12.5/lib64
```
Of course, if you use a different version of CUDA you will have to change ```12.5``` to the appropriate number.

To apply this run
```sh
source ~/.bashrc
```

## Pipeline dependencies
This is where using the older version of CUDA toolkit caused issues for me.

Install ```git```.
```sh
sudo apt-get install git
```
### PSRDADA
This ran smoothly once we had updated to the newest version of CUDA toolkit (12.5)

To keep it organised make a folder somewhere where this will take place. They recommend doing it in your home directory
```sh
cd && mkdir src && cd src
```

Clone PSRDADA
```sh
git clone git://git.code.sf.net/p/psrdada/code psrdada && cd psrdada
# Last tested version, bump as appropriate
git checkout 008afa7
```

Install some dependencies
```sh
sudo apt-get install build-essential cmake ninja-build -y
```

Build PSRDADA - this is where you will see issues if you're going to see any. It might be a matter of updating your CUDA or specifying which compilers to use in order to fix any issues you encounter.
```sh
mkdir build && cd build
cmake -GNinja ..
ninja
sudo ninja install
```

To your ```~/.bashrc``` add
```
# PSRDADA
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
```
To apply this run
```
source ~/.bashrc
```

### Heimdall
Back in the ```~/src``` directory clone the GReX fork of Heimdall.
```sh
git clone --recurse-submodules  https://github.com/GReX-Telescope/heimdall-astro
cd heimdall-astro
```
Install some dependencies
```sh
sudo apt-get install libboost-all-dev -y
```

At this point when following the instructions from the GReX team we ran into an error with the compilers, the solution we found was to rename the file ```heimdall-astro/Applications/heimdall.cpp``` to ```heimdall-astro/Applications/heimdall.cu```.
```sh
mv ~/src/heimdall-astro/Applications/heimdall.cpp ~/src/heimdall-astro/Applications/heimdall.cu
```

Then, at the top of the file ```~/src/heimdall-astro/Applications/CMakeLists.txt``` replace ```add_executable(heimdall heimdall.cpp)``` with ```add_executable(heimdall heimdall.cu)```

After this you should be ok to continue with the instructions as laid out by the GReX team
```sh
cd ~/src/heimdall-astro
mkdir build && cd build
cmake -GNinja ..
ninja
```

If this works successfully then running ```./dedisp/testdedisp``` should return
```sh
----------------------------- INPUT DATA ---------------------------------
Frequency of highest chanel (MHz)            : 1581.0000
Bandwidth (MHz)                              : 100.00
NCHANS (Channel Width [MHz])                 : 1024 (-0.097656)
Sample time (after downsampling by 1)        : 0.000250
Observation duration (s)                     : 30.000000 (119999 samples)
Data RMS ( 8 bit input data)                 : 25.000000
Input data array size                        : 468 MB

Embedding signal
----------------------------- INJECTED SIGNAL  ----------------------------
Pulse time at f0 (s)                      : 3.141590 (sample 12566)
Pulse DM (pc/cm^3)                        : 41.159000
Signal Delays : 0.000000, 0.000008, 0.000017 ... 0.009530
Rawdata Mean (includes signal)    : -0.002202
Rawdata StdDev (includes signal)  : 25.001451
Pulse S/N (per frequency channel) : 1.000000
Quantizing array
Quantized data Mean (includes signal)    : 127.497818
Quantized data StdDev (includes signal)  : 25.003092

Init GPU
Create plan
Gen DM list
----------------------------- DM COMPUTATIONS  ----------------------------
Computing 32 DMs from 2.000000 to 102.661667 pc/cm^3
Max DM delay is 95 samples (0 seconds)
Computing 119904 out of 119999 total samples (99.92% efficiency)
Output data array size : 14 MB

Compute on GPU
Dedispersion took 0.02 seconds
Output RMS                               : 0.376464
Output StdDev                            : 0.002307
DM trial 11 (37.681 pc/cm^3), Samp 12566 (3.141500 s): 0.390678 (6.16 sigma)
DM trial 11 (37.681 pc/cm^3), Samp 12567 (3.141750 s): 0.398160 (9.41 sigma)
DM trial 11 (37.681 pc/cm^3), Samp 12568 (3.142000 s): 0.393198 (7.25 sigma)
DM trial 11 (37.681 pc/cm^3), Samp 12569 (3.142250 s): 0.391713 (6.61 sigma)
DM trial 12 (40.926 pc/cm^3), Samp 12566 (3.141500 s): 0.441719 (28.29 sigma)
DM trial 13 (44.171 pc/cm^3), Samp 12564 (3.141000 s): 0.400574 (10.45 sigma)
DM trial 13 (44.171 pc/cm^3), Samp 12565 (3.141250 s): 0.403097 (11.55 sigma)
Dedispersion successful.
```

Then finally install it with
```sh
sudo ninja install
```

### HDF5/NetCDF
Install this with
```sh
sudo apt-get install libhdf5-dev libnetcdf-dev -y
```

## Rust
Install Rust using the default settings.
```sh
sudo apt-get install curl -y
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
Then press enter when prompted.

Then run what Rust prompts you to depending on your system.

## Python

### Install python 3.10
Later, when you go to clone and build the pipline software you may get an error which states that the software requires a python version ```>=3.9,<3.11``` depending on the version of python your Ubuntu install came with. Ours came with version 3.12.3, so it was necessary to downgrade it. We chose the newest version of python 3.10 which was specifically 3.10.14 at the time of writing. The commands below install that version of python, make it the default when using ```python3``` and then build the pipeline software.
```sh
cd /tmp
wget https://www.python.org/ftp/python/3.10.14/Python-3.10.14.tgz
tar -xf Python-3.10.14.tgz
cd Python-3.10.14
./configure --enable-optimizations
sudo make install
```
### Install Poetry
Poetry is a version control system for python it needs to be installed with

```sh
curl -sSL https://install.python-poetry.org | python3 -
```

To your ```~/.bashrc``` add
```sh
# Poetry
export PATH="/home/user/.local/bin:$PATH"
# Fix the "Poetry: Failed to unlock the collection" issue
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
```


To apply this run
```sh
source ~/.bashrc
```

## Pipeline software
To install this run

```sh
cd
git clone --recurse-submodules https://github.com/GReX-Telescope/grex
cd grex
./build.sh
```

If there are errors with including files when running ```./build.sh``` the files may exist elsewhere on your system where they are not being included from, to check if this is the case run

```sh
locate <file_name>
```

If this is the case you can make soft links between the location the program is looking for the files in and the files using

```sh
ln -s path/to/actual/file/location path/to/location/program/is/looking/for/file/in
```

Specifically for us the files that were not found initially were ```stdarg.h``` and ```stddef.h```. Locating both of these files gave a number of different locations and files, however the specific files we linked were ```/usr/lib/gcc/x86_64-linux-gnu/14/include/stdarg.h``` and ```/usr/lib/gcc/x86_64-linux-gnu/14/include/stddef.h```.


Then the ```parallel``` package must be installed.
```sh
sudo apt install parallel -y
```


See [Operation.md](https://github.com/ismisebrendan/GReX_setup/new/main) for information on how to run the pipeline.

A ```.env``` file in the same directory as ```grex.sh``` can be used to define settings for the pipeline preventing the need to constantly define the settings each time the pipeline is run.

## Databases and Metrics Collection
### Docker
Install Docker as detailed [here](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository). We used the ```apt``` method, however there are other methods.

This is a summary of all the commands necessary for this method
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

Then test by running
```sh
sudo docker run hello-world
```

### Observability Stack

Have not done this yet, this is for setting up grafana for monitoring





