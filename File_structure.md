# Required default file structure

## Saving data
By default data is saved to ```/hdd/data/```.

Within ```/hdd/data/``` there should be the file ```candidates.db``` and the directories:
 - ```filterbanks/```
 - ```voltages/```
 - ```candidates/```
 - ```candidates/T2/```

```candidates.db``` can be created empty, the pipeline will fill it automatically.

## Injected pulses
The default directory that the pipeline looks for pulses to inject is ```path/to/pipeline/script/fake/```. It takes ```.dat``` files as the input for the injected pulses.