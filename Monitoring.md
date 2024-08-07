To monitor that different parts of the GReX are working you can ping the Raspberry Pi in the GReX with

```sh
ping 192.168.0.2
```

or ping the SNAP itself

```sh
ping 192.168.0.3
```

Also, once you have connected to the GReX pi via ssh you can run

```sh
./cli /dev/serial0 mon
```

to monitor the current and voltage going to the LNAs. An example output is

```sh
[cli/src/main.rs:91] write_read(&transport::Command::Monitor, port) = Some(
    Monitor(
        MonitorPayload {
            if1_power: -1.3686428,
            if2_power: -1.1438046,
            ic_temp: 49.609035,
            lna1_power: Power {
                voltage: 5.392,
                current: 0.067719996,
            },
            lna2_power: Power {
                voltage: 5.352,
                current: 0.07408,
            },
            analog_power: Power {
                voltage: 4.912,
                current: 0.5704,
            },
        },
    ),
)
```

Ideally the LNA currents should be around 60-70 mA.
