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
[ 7093.213489] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7093.421376] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7093.525255] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7093.941196] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7094.045471] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
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
[ 7098.389112] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7098.597411] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7098.805347] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7099.117228] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7099.221034] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7099.845061] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7100.365001] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7100.573377] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7100.780986] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7101.093041] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7101.509084] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7101.821031] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7102.653319] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7103.277005] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
[ 7103.588967] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Down
[ 7103.797039] ixgbe 0000:01:00.0 enp1s0f0: NIC Link is Up 10 Gbps, Flow Control: RX/TX
```

### Solution
Upon speaking to Kiran Shila, one of the creators of GReX, and showing him the above output he was able to tell us it was a problem with our optics. As it happens, the optics installed in our server and GReX unit are 10 km optics. As we were using a 25 m long cable this meant we were oversaturating the optics and causing issues due to this.

The solution is to use more appropriate optical or copper connections.


