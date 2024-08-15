# Troubleshooting

## Initial difficulties communicating with the GReX

### Issue
When first setting up the server we were unable to communicate with the GReX over the fiber connection. Upon pinging the raspberry pi on ```192.168.0.2``` we would get

```sh
ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=2 ttl=64 time=0.702 ms
64 bytes from 192.168.0.2: icmp_seq=3 ttl=64 time=0.707 ms
From 192.168.0.1 icmp_seq=4 Destination Host Unreachable
64 bytes from 192.168.0.2: icmp_seq=5 ttl=64 time=0.690 ms
From 192.168.0.1 icmp_seq=10 Destination Host Unreachable
From 192.168.0.1 icmp_seq=11 Destination Host Unreachable
From 192.168.0.1 icmp_seq=12 Destination Host Unreachable
From 192.168.0.1 icmp_seq=13 Destination Host Unreachable
64 bytes from 192.168.0.2: icmp_seq=17 ttl=64 time=0.450 ms
64 bytes from 192.168.0.2: icmp_seq=18 ttl=64 time=0.732 ms
```

i.e. a lot of ```Destination Host Unreachable``` messages, along with a lot of dropped packages altogether.

Running a test command ```dmesg | grep -e ixgbe -e enp1s``` the response we got was

```sh
[ 7094.149082] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7094.253430] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7094.669384] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7094.981233] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7095.189367] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7095.293221] ixgbe 0000:01:00.0 enp1s0f0: initiating reset to clear Tx work after link loss
[ 7095.397354] ixgbe 0000:01:00.0 enp1s0f0: Reset adapter
[ 7096.114824] ixgbe 0000:01:00.0 enp1s0f0: detected SFP+: 5
[ 7096.212990] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7096.278517] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7098.285421] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
```

### Solution
Upon speaking to Kiran Shila, one of the creators of GReX, and showing him the above output he was able to tell us it was a problem with our optics. As it happens, the optics installed in our server and GReX unit are 10 km optics. As we were using a 25 m long cable this meant we were oversaturating the optics and causing issues due to this.

The solution is to use more appropriate optical or copper connections.

## Pipeline not running

There are a number of reasons why this might be:

### The file structure is not correct

If the file structure is not correct the pipeline will crash on trying to read data from a non-existent file or on trying to write to a non-existent directory. See [File_structure.md](https://github.com/ismisebrendan/GReX_Birr_setup/blob/main/File_structure.md) for the details of the file structure necessary.

### Cannot connect to network time protocol

Trinity appears to have blocked ```time.google.com``` which is the default NTP server for GReX. When calling ```./grex.sh``` the flags ```-st``` or ```--skip_ntp``` can be used to skip NTP synchronisation to avoid this, because otherwise if it cannot contact the server it will crash the program.

### Switch not set up correctly

If, upon running ```iftop -i [port-to-GReX]``` there doesn't appear to be any data flowing between the GReX and the server it might be the case that the switch in the GReX was not configured correctly.

To fix this you need to access the GReX switch GUI, which if you are physically at the server is accessible in a web browser at ```192.168.88.1```, or if you are accessing the server remotely you must first forward that IP's port 80 to your local computer at some unused, non-privaleged port (such as 8080). This is detailed in the [operation](https://grex-telescope.github.io/software/operation/) page on the GReX website. the command is
```sh
ssh -L 8080:192.168.88.1:80 username@grex-server-address
```

Then go to localhost:8080 in a web browser and enter the switch's control panel. If it looks like this, with the Actual MTU columns being 9000 and L2 MTU being 9216 then the switch is configured correctly






