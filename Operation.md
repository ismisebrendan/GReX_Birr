# Running the pipeline

The pipline can be run by running ```~/grex/pipeline/grex.sh```.

To run the pipeline software there must be a database file for it to use. By default this is in ```/hdd/data/candidates.db``` but can be set with flags when running ```./grex.sh```. The flags are ```-dbp``` or ```--db_path``` (they are equivalent).

More flags can be see by running ```./grex.sh -h```.

Trinity appears to have blocked ```time.google.com``` which is the default NTP server for GReX. When calling ```./grex.sh``` the flags ```-st``` or ```--skip_ntp``` can be used to skip NTP synchronisation to avoid this, because otherwise if it cannot contact the server it will crash the program.

The pipline requires the injection of pulses, taken from a ```.dat``` file in ```~/grex/pipeline/fake```. However if an empty ```.dat``` file is provided it doesn't raise any errors.
