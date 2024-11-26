# The current problems with the GReX setup

Automatic plotting and reporting of candidates using T3 is not working. What I have done so far, written as instructions is shown below. I imagine it's a case of some dependencies or something not working, but there isn't much about T3 out there and I've not been able to get much from the GReX team about it.

---

In ```~/grex/``` make a new directory ```t3/``` and in here run

```sh
git clone https://github.com/GReX-Telescope/GReX-T3
```

Within this directory go to ```GReX-T3/grex_t3/``` and edit ```T3_monitor.py```. Here you should replace

```sh
logfile = '/home/user/zghuai/GReX-T3/services/T3_plotter.log'
env_dir = "/home/user/zghuai/GReX-T3/grex_t3/"
mon_dir = "/hdd/data/voltages/" # monitoring dir
dir_plot = "/hdd/data/candidates/T3/candplots/" # place to save output plots
dir_fil  = "/hdd/data/candidates/T3/candfils/"  # place to save output filterbank files
```

Also modify ```T3_manager.py``` and replace

```sh
FILPATH = '/home/liam/grexdata/'
OUTPUT_PATH = '/home/liam/grexdata/output'
```

with the appropriate paths for the local system.

with the appropriate paths for your set-up (although it is probably easiest if you leave the third to fifth lines here as they are.

Then copy the files ```~/grex/t3/GReX-T3/services/cand_plotter.service``` and ```~/grex/t3/GReX-T3/services/clear_disks.service``` to ```/etc/systemd/system/``` and in them change the lines pointing to directories to correspond to your own system.

Within ```~/grex/t3/GReX-T3``` run

```sh
poetry install
```


The pipeline can be run by running ```~/grex/pipeline/grex.sh```.
